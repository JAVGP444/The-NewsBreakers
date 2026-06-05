"""Contraste con feeds oficiales WOAH / OMS / CDC."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CACHE = ROOT / "data" / "raw" / "official_feeds.json"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

try:
    from official_scraper import fetch_all_feeds, match_against_official
except ImportError:
    fetch_all_feeds = None  # type: ignore
    match_against_official = None  # type: ignore


def _load_cache() -> dict[str, Any] | None:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def check_official_alignment(text: str) -> dict[str, Any]:
    feeds = _load_cache()
    if feeds is None and fetch_all_feeds:
        try:
            feeds = fetch_all_feeds()
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(feeds, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            feeds = {"relevant_items": []}

    if not feeds or not match_against_official:
        return {
            "official_matches": [],
            "feed_count": 0,
            "has_official_alignment": False,
            "score_delta": 0,
            "source": "unavailable",
        }

    result = match_against_official(text, feeds)
    result["source"] = "cache" if _load_cache() else "live"
    return result
