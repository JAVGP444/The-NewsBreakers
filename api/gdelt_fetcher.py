"""Cliente GDELT — contraste con cobertura mediática global."""

from __future__ import annotations

import re
from typing import Any

import httpx

GDELT_DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"

DEFAULT_QUERY = (
    '(avian flu OR "avian influenza" OR H5N1 OR "african swine fever" OR '
    '"gripe aviar" OR "peste porcina" OR WOAH OR "animal outbreak")'
)


def build_query_from_text(text: str, extra_terms: list[str] | None = None) -> str:
    terms: list[str] = []
    if extra_terms:
        terms.extend(extra_terms[:5])

    for token in re.findall(r"\bH5N\d|H7N\d|ASF|FMD|BSE\b", text, re.I):
        terms.append(token.upper())

    lowered = text.lower()
    for phrase in [
        "avian flu", "bird flu", "gripe aviar", "african swine fever",
        "peste porcina", "foot and mouth", "fiebre aftosa", "lumpy skin",
    ]:
        if phrase in lowered:
            terms.append(f'"{phrase}"')

    if not terms:
        return DEFAULT_QUERY

    unique = list(dict.fromkeys(terms))
    return " OR ".join(unique[:6])


def search_animal_health(
    query: str | None = None,
    max_records: int = 8,
    timespan: str = "7d",
) -> list[dict[str, Any]]:
    params = {
        "query": query or DEFAULT_QUERY,
        "mode": "ArtList",
        "maxrecords": max_records,
        "format": "json",
        "timespan": timespan,
        "sort": "datedesc",
    }
    try:
        with httpx.Client(timeout=25.0) as client:
            r = client.get(GDELT_DOC_API, params=params)
            r.raise_for_status()
            data = r.json()
            articles = data.get("articles", [])
            return [
                {
                    "title": a.get("title", ""),
                    "url": a.get("url", ""),
                    "domain": a.get("domain", ""),
                    "seendate": a.get("seendate", ""),
                    "language": a.get("language", ""),
                    "sourcecountry": a.get("sourcecountry", ""),
                }
                for a in articles
            ]
    except Exception:
        return []


def assess_corroboration(
    text: str,
    topic_matches: list[str],
    alarm_matches: list[str],
) -> dict[str, Any]:
    query = build_query_from_text(text, topic_matches[:5])
    articles = search_animal_health(query=query, max_records=8)

    text_lower = text.lower()
    overlap_titles = []
    trusted_domains = {"reuters.com", "bbc.com", "who.int", "woah.org", "cdc.gov", "fao.org", "apnews.com"}

    for article in articles:
        title_lower = article.get("title", "").lower()
        domain = article.get("domain", "").lower()
        shared = [t for t in topic_matches if t.lower() in title_lower or t.lower() in text_lower]
        if shared or any(td in domain for td in trusted_domains):
            overlap_titles.append(article)

    has_coverage = len(articles) >= 2
    has_trusted = any(
        any(td in a.get("domain", "").lower() for td in trusted_domains)
        for a in articles
    )
    claims_outbreak = bool(topic_matches) and any(
        w in text_lower for w in ["brote", "outbreak", "surto", "épidémie", "epidemic", "pandemic", "pandemia"]
    )

    score_delta = 0
    status = "no_data"

    if has_coverage and has_trusted:
        score_delta = 18
        status = "corroborated"
    elif has_coverage:
        score_delta = 10
        status = "partial_coverage"
    elif claims_outbreak and not alarm_matches:
        score_delta = -8
        status = "unverified_claim"
    elif claims_outbreak and alarm_matches:
        score_delta = -12
        status = "alarm_without_coverage"

    return {
        "status": status,
        "score_delta": score_delta,
        "query_used": query,
        "articles_found": len(articles),
        "trusted_sources_in_results": has_trusted,
        "related_articles": articles[:5],
        "overlap_articles": overlap_titles[:3],
    }
