"""
Scraper de fuentes oficiales — WOAH, OMS (WHO), CDC.
Uso: python tools/official_scraper.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

import httpx

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "raw" / "official_feeds.json"

FEEDS = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "CDC": "https://tools.cdc.gov/api/v2/resources/media/403372.rss",
    "WOAH": "https://www.woah.org/en/rss/",
}

HEADERS = {"User-Agent": "TheNewsBreakers/1.0 (datathon; animal-health-verification)"}

ANIMAL_KEYWORDS = re.compile(
    r"avian|flu|influenza|H5N1|swine|livestock|poultry|animal|zoono|"
    r"epizoo|outbreak|veterinar|gripe|porcina|aftosa|woah|fao|"
    r"ganado|aves|cerdo|bovine|rabies|brucell",
    re.I,
)


def parse_rss(xml_text: str, source: str, limit: int = 15) -> list[dict]:
    items = []
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return items

    for item in root.findall(".//item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or item.findtext("date") or "").strip()
        desc = re.sub(r"<[^>]+>", " ", item.findtext("description") or "")
        desc = re.sub(r"\s+", " ", desc).strip()[:300]
        if title:
            items.append({
                "source": source,
                "title": title,
                "link": link,
                "published": pub,
                "summary": desc,
                "relevant": bool(ANIMAL_KEYWORDS.search(f"{title} {desc}")),
            })
    return items


def fetch_woah_fallback(client: httpx.Client) -> list[dict]:
    """WOAH RSS a veces falla; fallback a página de noticias."""
    url = "https://www.woah.org/en/media-center/news/"
    try:
        r = client.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        titles = re.findall(r'<h[23][^>]*class="[^"]*title[^"]*"[^>]*>\s*([^<]+)\s*<', r.text, re.I)
        return [
            {
                "source": "WOAH",
                "title": t.strip(),
                "link": url,
                "published": "",
                "summary": "",
                "relevant": bool(ANIMAL_KEYWORDS.search(t)),
            }
            for t in titles[:12]
        ]
    except Exception:
        return []


def fetch_all_feeds() -> dict:
    results: dict[str, list] = {"fetched_at": datetime.now(timezone.utc).isoformat(), "items": []}

    with httpx.Client(timeout=25.0, follow_redirects=True) as client:
        for source, feed_url in FEEDS.items():
            try:
                r = client.get(feed_url, headers=HEADERS)
                r.raise_for_status()
                items = parse_rss(r.text, source)
                if source == "WOAH" and not items:
                    items = fetch_woah_fallback(client)
                results["items"].extend(items)
            except Exception as exc:
                if source == "WOAH":
                    results["items"].extend(fetch_woah_fallback(client))
                results.setdefault("errors", []).append({source: str(exc)})

    results["relevant_items"] = [i for i in results["items"] if i.get("relevant")]
    return results


def match_against_official(text: str, feeds: dict | None = None) -> dict:
    if feeds is None:
        feeds = fetch_all_feeds()

    text_lower = text.lower()
    matches = []
    for item in feeds.get("relevant_items", []):
        title_lower = item["title"].lower()
        tokens = [w for w in re.findall(r"\w{5,}", title_lower) if w in text_lower]
        if tokens or any(k in text_lower for k in ["h5n1", "avian", "gripe aviar", "swine", "porcina"]):
            matches.append({**item, "matched_tokens": tokens[:5]})

    return {
        "official_matches": matches[:5],
        "feed_count": len(feeds.get("relevant_items", [])),
        "has_official_alignment": len(matches) > 0,
        "score_delta": 15 if matches else 0,
    }


def main() -> None:
    data = fetch_all_feeds()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Guardado: {OUTPUT}")
    print(f"Total: {len(data['items'])} | Relevantes salud animal: {len(data['relevant_items'])}")


if __name__ == "__main__":
    main()
