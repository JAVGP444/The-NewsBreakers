"""Motor de análisis multilingüe — The NewsBreakers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from langdetect import DetectorFactory, detect

from gdelt_fetcher import assess_corroboration
from official_checker import check_official_alignment

DetectorFactory.seed = 0

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
SUPPORTED_LANGUAGES = {"es", "en", "fr", "pt", "de", "it", "zh", "ar", "ru", "ja"}


def _load_yaml(name: str) -> dict[str, Any]:
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except Exception:
        return "en"


def _find_matches(text: str, keywords: list[str]) -> list[str]:
    lower = text.lower()
    return [kw for kw in keywords if kw.lower() in lower]


def _alarm_density(text: str, alarm_kws: list[str]) -> float:
    if not alarm_kws:
        return 0.0
    lower = text.lower()
    hits = sum(1 for kw in alarm_kws if kw.lower() in lower)
    return min(hits / max(len(text.split()), 1) * 100, 1.0)


def _has_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\])\"']+", text, flags=re.IGNORECASE)


def _domain_from_url(url: str) -> str:
    m = re.search(r"https?://(?:www\.)?([^/]+)", url, re.IGNORECASE)
    return m.group(1).lower() if m else ""


def _match_domains(urls: list[str], domains: list[str]) -> list[str]:
    matched = []
    for url in urls:
        domain = _domain_from_url(url)
        if any(d in domain for d in domains):
            matched.append(url)
    return matched


def _sensationalism_score(text: str) -> int:
    flags = 0
    if text != text.lower() and sum(1 for c in text if c.isupper()) > len(text) * 0.25:
        flags += 1
    if text.count("!") >= 3:
        flags += 1
    if re.search(r"\b(URGENT|BREAKING|ALERTA|ÚLTIMA HORA|COMPARTE|SHARE NOW)\b", text, re.I):
        flags += 1
    if re.search(r"[A-ZÁÉÍÓÚÑ]{8,}", text):
        flags += 1
    return flags


def _lab_confirmed(text: str, lang: str) -> bool:
    patterns = [
        r"laboratorio confirm", r"laboratory confirm", r"lab.?confirmed",
        r"confirmado por laboratorio", r"caso confirmado", r"confirmed case",
    ]
    return any(re.search(p, text, re.I) for p in patterns)


def _build_score_breakdown(
    indicators: dict[str, Any],
    gdelt: dict[str, Any],
    official: dict[str, Any],
    cfg: dict[str, Any],
) -> tuple[int, list[dict[str, Any]]]:
    weights = cfg.get("weights", {})
    penalties = cfg.get("penalties", {})
    base = cfg.get("base_score", 45)
    score = base
    breakdown: list[dict[str, Any]] = [{"label": "Base neutral", "delta": base}]

    def add(label: str, delta: int) -> None:
        nonlocal score
        if delta:
            score += delta
            breakdown.append({"label": label, "delta": delta})

    if indicators["topic_matches"]:
        add("Tema salud animal detectado", weights.get("has_topic_keywords", 0))
    if len(indicators["topic_matches"]) >= 3:
        add("Múltiples términos veterinarios", weights.get("multiple_topic_keywords", 0))
    if not indicators["topic_matches"]:
        add("Fuera de tema / sin keywords", penalties.get("off_topic", 0))

    if indicators["trust_matches"]:
        add("Señales de credibilidad", weights.get("has_trust_signals", 0))
    if indicators["official_links"]:
        add("Enlaces a dominios oficiales", weights.get("has_official_domain_link", 0))
    if indicators["fact_check_links"]:
        add("Enlaces a verificadores (IFCN)", weights.get("fact_check_domain_link", 0))
    if indicators["urls"]:
        add("Incluye URLs citadas", weights.get("has_cited_urls", 0))
    else:
        add("Sin fuentes enlazadas", penalties.get("no_sources", 0))

    if indicators["alarm_density"] < 0.05:
        add("Baja densidad de alarma", weights.get("low_alarm_density", 0))
    elif indicators["alarm_density"] > 0.12:
        add("Alta densidad de alarma", penalties.get("high_alarm_density", 0))

    if indicators["alarm_matches"] and not indicators["trust_matches"]:
        add("Lenguaje conspirativo sin respaldo", penalties.get("conspiracy_language", 0))
    if indicators["sensationalism_flags"] >= 2:
        add("Sensacionalismo elevado", penalties.get("sensationalism_high", 0))
    if indicators["laboratory_confirmed"]:
        add("Confirmación de laboratorio", weights.get("laboratory_confirmed", 0))

    add("Cobertura GDELT global", gdelt.get("score_delta", 0))
    if gdelt.get("status") == "alarm_without_coverage":
        add("Alarma sin cobertura mediática", penalties.get("gdelt_no_coverage_claim", 0))

    add("Alineación feeds oficiales", official.get("score_delta", 0))

    score = max(0, min(100, score))
    return score, breakdown


def analyze_text(text: str, use_gdelt: bool = True, use_official: bool = True) -> dict[str, Any]:
    keywords_cfg = _load_yaml("keywords.yaml")
    indicators_cfg = _load_yaml("indicators.yaml")
    trusted_cfg = _load_yaml("trusted_sources.yaml")

    lang = detect_language(text)

    topic_lang = keywords_cfg.get("topic_keywords", {}).get(lang, [])
    topic_en = keywords_cfg.get("topic_keywords", {}).get("en", [])
    topic_matches = _find_matches(text, list(dict.fromkeys(topic_lang + topic_en)))

    alarm_kws = keywords_cfg.get("alarm_keywords", {}).get(lang, [])
    alarm_kws += keywords_cfg.get("alarm_keywords", {}).get("en", [])
    alarm_matches = _find_matches(text, list(dict.fromkeys(alarm_kws)))

    trust_kws = keywords_cfg.get("trust_signals", {}).get(lang, [])
    trust_kws += keywords_cfg.get("trust_signals", {}).get("en", [])
    trust_matches = _find_matches(text, list(dict.fromkeys(trust_kws)))

    urls = _has_urls(text)
    official_links = _match_domains(urls, trusted_cfg.get("official_domains", []))
    fact_check_links = _match_domains(urls, trusted_cfg.get("fact_check_domains", []))
    alarm_density = _alarm_density(text, alarm_kws)
    sensationalism = _sensationalism_score(text)
    lab_confirmed = _lab_confirmed(text, lang)

    gdelt = assess_corroboration(text, topic_matches, alarm_matches) if use_gdelt else {
        "status": "skipped", "score_delta": 0, "related_articles": [], "articles_found": 0,
    }
    official = check_official_alignment(text) if use_official else {
        "official_matches": [], "has_official_alignment": False, "score_delta": 0,
    }

    indicators = {
        "language": lang,
        "topic_matches": topic_matches[:12],
        "alarm_matches": alarm_matches[:8],
        "trust_matches": trust_matches[:8],
        "urls": urls,
        "official_links": official_links,
        "fact_check_links": fact_check_links,
        "alarm_density": round(alarm_density, 4),
        "sensationalism_flags": sensationalism,
        "laboratory_confirmed": lab_confirmed,
        "word_count": len(text.split()),
        "gdelt_status": gdelt.get("status"),
        "gdelt_articles_found": gdelt.get("articles_found", 0),
        "official_feed_alignment": official.get("has_official_alignment", False),
    }

    score, breakdown = _build_score_breakdown(indicators, gdelt, official, indicators_cfg)
    thresholds = indicators_cfg.get("verdict_thresholds", {})
    labels = indicators_cfg.get("verdict_labels", {})

    if score >= thresholds.get("reliable", 72):
        verdict = "reliable"
    elif score >= thresholds.get("uncertain", 45):
        verdict = "uncertain"
    else:
        verdict = "suspicious"

    verdict_es = labels.get(verdict, {}).get("es", verdict)

    recommendations = _build_recommendations(indicators, gdelt, official, verdict)

    return {
        "team": "The NewsBreakers",
        "product": "Animal Health Misinformation Verifier",
        "indicators": indicators,
        "score": score,
        "score_breakdown": breakdown,
        "verdict": verdict,
        "verdict_es": verdict_es,
        "recommendations": recommendations,
        "gdelt": {
            "status": gdelt.get("status"),
            "query": gdelt.get("query_used", ""),
            "articles_found": gdelt.get("articles_found", 0),
            "trusted_in_results": gdelt.get("trusted_sources_in_results", False),
            "related_articles": gdelt.get("related_articles", []),
        },
        "official_sources": {
            "aligned": official.get("has_official_alignment", False),
            "matches": official.get("official_matches", []),
            "feed_count": official.get("feed_count", 0),
        },
        "trusted_domains": trusted_cfg.get("official_domains", [])[:6],
        "fact_check_domains": trusted_cfg.get("fact_check_domains", [])[:4],
    }


def _build_recommendations(
    indicators: dict[str, Any],
    gdelt: dict[str, Any],
    official: dict[str, Any],
    verdict: str,
) -> list[str]:
    recs = []

    if not indicators["topic_matches"]:
        recs.append("El contenido no referencia claramente enfermedades o brotes en animales.")
    if indicators["alarm_matches"]:
        recs.append("Se detectó vocabulario de alarma o conspiración. Contrastar con WOAH y OMS.")
    if not indicators["trust_matches"] and not indicators["official_links"]:
        recs.append("No hay citas explícitas a organismos oficiales ni enlaces verificables.")
    if indicators["sensationalism_flags"] >= 2:
        recs.append("Tono sensacionalista: priorizar fuentes primarias y datos de laboratorio.")
    if gdelt.get("status") == "corroborated":
        recs.append("GDELT muestra cobertura global reciente coherente con el tema.")
    elif gdelt.get("status") == "alarm_without_coverage":
        recs.append("Afirmación alarmante sin respaldo en cobertura mediática global (GDELT).")
    elif gdelt.get("status") == "unverified_claim":
        recs.append("Afirma un brote sin cobertura GDELT reciente — verificar con WOAH/CDC.")
    if official.get("has_official_alignment"):
        recs.append("Existen titulares oficiales recientes relacionados con este tema.")
    if verdict == "reliable":
        recs.append("Verifica fecha, ubicación geográfica y número de casos en el informe original.")
    if verdict == "suspicious":
        recs.append("No difundir sin contrastar con al menos dos fuentes oficiales certificadas.")

    return recs
