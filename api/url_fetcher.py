"""Extrae texto de URLs para análisis."""

from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup


def extract_text_from_url(url: str, timeout: float = 15.0) -> tuple[str, dict]:
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL debe comenzar con http:// o https://")

    headers = {"User-Agent": "TheNewsBreakers/0.1 (datathon)"}

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""
    article = soup.find("article")
    body = article.get_text(separator=" ", strip=True) if article else soup.get_text(separator=" ", strip=True)
    body = re.sub(r"\s+", " ", body).strip()

    if len(body) < 50:
        raise ValueError("No se pudo extraer suficiente texto de la URL")

    text = f"{title}\n\n{body}" if title else body
    meta = {"title": title, "chars_extracted": len(body)}
    return text[:15000], meta
