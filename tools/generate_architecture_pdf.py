#!/usr/bin/env python3
"""Genera PDF de arquitectura técnica de The NewsBreakers."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "pdfs" / "Arquitectura-Tecnica-The-NewsBreakers.pdf"
FOOTER_DATE = "Junio 2026"


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, f"The NewsBreakers — Arquitectura Técnica · {FOOTER_DATE}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "DocTitle",
            parent=base["Title"],
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor("#0a2540"),
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base["Normal"],
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor("#425466"),
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontSize=16,
            leading=20,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#0a2540"),
            borderPadding=4,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#1a3a5c"),
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=9.5,
            leading=13,
            leftIndent=14,
            spaceAfter=3,
        ),
        "toc": ParagraphStyle(
            "TOC",
            parent=base["Normal"],
            fontSize=10,
            leading=16,
            leftIndent=8,
        ),
        "mono": ParagraphStyle(
            "Mono",
            parent=base["Code"],
            fontSize=8,
            leading=10,
            fontName="Courier",
            spaceAfter=4,
        ),
    }


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(text, style)


def _table(data: list[list[str]], col_widths: list[float] | None = None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a2540")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d0d7de")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fa")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def build_story(s: dict) -> list:
    story: list = []

    # ── Portada ──
    story.append(Spacer(1, 4 * cm))
    story.append(_p("The NewsBreakers", s["title"]))
    story.append(_p("Arquitectura Técnica", s["title"]))
    story.append(Spacer(1, 0.8 * cm))
    story.append(_p("Verificador de desinformación en salud animal y brotes epizoóticos", s["subtitle"]))
    story.append(_p("Documento para portfolio y Q&A de presentación", s["subtitle"]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(_p(f"Versión 1.1.0 · {FOOTER_DATE}", s["subtitle"]))
    story.append(_p("Equipo: The NewsBreakers", s["subtitle"]))
    story.append(PageBreak())

    # ── Índice ──
    story.append(_p("Tabla de contenidos", s["h1"]))
    toc_items = [
        "1. Resumen ejecutivo",
        "2. Objetivo y problema que resuelve",
        "3. Arquitectura general",
        "4. Frontend (Next.js, puerto 3003)",
        "5. Backend (FastAPI, puerto 8000)",
        "6. Base de datos y almacenamiento",
        "7. Librerías Python",
        "8. Librerías JavaScript / Node",
        "9. Flujo de verificación de noticias",
        "10. Fuentes de datos",
        "11. IA, Ollama y análisis local",
        "12. Extensión Chrome",
        "13. Scripts de despliegue local",
        "14. Estructura de carpetas",
        "15. Endpoints API",
        "16. Equipo y colaboración",
        "17. Tecnologías NO usadas",
    ]
    for item in toc_items:
        story.append(_p(item, s["toc"]))
    story.append(PageBreak())

    # ── 1. Resumen ──
    story.append(_p("1. Resumen ejecutivo", s["h1"]))
    story.append(
        _p(
            "<b>The NewsBreakers</b> es un verificador profesional de desinformación en salud animal, "
            "brotes epizoóticos y zoónosis. Permite analizar texto o URL y devuelve un veredicto explicable "
            "(real, falso, no verificada, dudosa) con puntuación 0–100, evidencia enlazada y recomendaciones.",
            s["body"],
        )
    )
    story.append(
        _p(
            "La solución combina un frontend Next.js 15 + React 19 (puerto 3003), una API REST FastAPI + uvicorn "
            "(puerto 8000), un motor de análisis modular en Python, una extensión Chrome Manifest V3, "
            "configuración declarativa en YAML y almacenamiento en archivos JSON.",
            s["body"],
        )
    )

    # ── 2. Objetivo ──
    story.append(_p("2. Objetivo y problema que resuelve", s["h1"]))
    story.append(_p("Problema", s["h2"]))
    story.append(
        _p(
            "Circulan afirmaciones alarmistas sobre brotes, transmisión alimentaria y pandemias animales "
            "sin respaldo en organismos oficiales (OMS/WHO, WOAH, CDC, FAO), con lenguaje sensacionalista.",
            s["body"],
        )
    )
    story.append(_p("Objetivo", s["h2"]))
    for b in [
        "Detectar idioma y tema veterinario/epidemiológico (hasta 10 idiomas).",
        "Extraer afirmaciones concretas: enfermedad, ubicación, fechas, instituciones.",
        "Buscar evidencia en internet: portales oficiales, GDELT, Wikipedia, fact-checkers.",
        "Evaluar con modelo de 4 pilares auditable y reglas de descarte R1–R9.",
        "Refinar opcionalmente con IA (Ollama/OpenAI/Anthropic) o análisis local.",
        "Presentar resultados en web y extensión de navegador.",
    ]:
        story.append(_p(f"• {b}", s["bullet"]))

    # ── 3. Arquitectura ──
    story.append(_p("3. Arquitectura general", s["h1"]))
    arch = """Usuario → Web (Next.js :3003) ──→ API (FastAPI :8000) ──→ Motor de análisis
                                              ├── claim_extractor (afirmaciones)
                                              ├── web_verifier + deep_verifier (internet)
                                              ├── gdelt_fetcher + trusted_search (GDELT, WHO, RSS)
                                              ├── investigation_evaluator (4 pilares)
                                              ├── ai_verifier (Ollama / OpenAI / local)
                                              └── sources_evaluator (150+ fuentes)
Extensión Chrome ──────────→ misma API (POST /analyze)
news_aggregator ───────────→ news_archive.json (refresh cada 15 min)"""
    for line in arch.split("\n"):
        story.append(_p(line, s["mono"]))

    story.append(_p("Principios de diseño", s["h2"]))
    story.append(
        _table(
            [
                ["Principio", "Implementación"],
                ["Separación de capas", "web/ (UI), api/ (lógica), config/ (datos)"],
                ["Evidencia primero", "Búsqueda web antes de solo keywords"],
                ["IA opcional", "Funciona sin API keys (análisis local)"],
                ["Misma API", "Web, extensión y clientes HTTP comparten endpoints"],
            ],
            [4.5 * cm, 12 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))

    # ── 4. Frontend ──
    story.append(_p("4. Frontend (Next.js)", s["h1"]))
    story.append(
        _table(
            [
                ["Tecnología", "Versión", "Uso"],
                ["Next.js", "^15.1.0", "App Router, SSR/CSR"],
                ["React", "^19.0.0", "UI declarativa"],
                ["TypeScript", "^5.7.2", "Tipado estático"],
                ["CSS propio", "—", "globals.css + dashboard.css"],
            ],
            [3.5 * cm, 2.5 * cm, 10.5 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(_p("Archivos clave: web/app/page.tsx (dashboard), AnalysisResults.tsx (veredicto), NewsCardItem.tsx, VerificationHistory.tsx (localStorage).", s["body"]))
    story.append(_p("Puerto: 3003. Variable: NEXT_PUBLIC_API_URL (default http://localhost:8000).", s["body"]))

    # ── 5. Backend ──
    story.append(_p("5. Backend (FastAPI)", s["h1"]))
    story.append(
        _table(
            [
                ["Módulo", "Responsabilidad"],
                ["analyzer.py", "Orquestador: idioma, YAML, veredicto final"],
                ["claim_extractor.py", "Extrae enfermedades, ubicaciones, instituciones"],
                ["web_verifier.py", "Búsqueda internet: GDELT, WHO, DuckDuckGo, RSS"],
                ["deep_verifier.py", "URLs en texto + news_archive.json"],
                ["ai_verifier.py", "OpenAI / Anthropic / Ollama / análisis local"],
                ["investigation_evaluator.py", "Modelo 4 pilares + reglas R1–R9"],
                ["sources_evaluator.py", "150+ fuentes gold/silver/bronze"],
                ["news_aggregator.py", "RSS + GDELT → news_archive.json"],
                ["gdelt_fetcher.py", "Cliente GDELT Doc API"],
                ["disease_catalog.py", "Catálogo de enfermedades desde YAML"],
                ["url_fetcher.py", "Extracción de texto de URLs"],
            ],
            [4.5 * cm, 12 * cm],
        )
    )

    story.append(PageBreak())

    # ── 6. Almacenamiento ──
    story.append(_p("6. Base de datos y almacenamiento", s["h1"]))
    story.append(_p("Lo que SÍ se usa", s["h2"]))
    story.append(
        _table(
            [
                ["Almacén", "Ubicación", "Propósito"],
                ["JSON noticias", "api/news_archive.json", "Histórico validado (máx. 500)"],
                ["YAML config", "config/*.yaml", "Keywords, fuentes, enfermedades"],
                ["localStorage", "Navegador", "Historial de verificaciones"],
                ["Logs", "logs/*.log", "Servicios en background"],
            ],
            [3 * cm, 5 * cm, 8.5 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(_p("Lo que NO se usa", s["h2"]))
    story.append(
        _p(
            "<b>SQLite:</b> no implementado (carpeta data/databases planificada, no existe en código). "
            "<b>pandas:</b> NO está en requirements.txt ni en ningún archivo del proyecto. "
            "<b>PostgreSQL, Redis, MongoDB:</b> no utilizados.",
            s["body"],
        )
    )

    # ── 7. Python libs ──
    story.append(_p("7. Librerías Python (api/requirements.txt)", s["h1"]))
    story.append(
        _table(
            [
                ["Librería", "Uso en el proyecto"],
                ["fastapi", "API REST, validación Pydantic, OpenAPI"],
                ["uvicorn", "Servidor ASGI"],
                ["pydantic", "Modelos de request/response"],
                ["langdetect", "Detección de idioma (10 idiomas)"],
                ["pyyaml", "Lectura de config/*.yaml"],
                ["httpx", "HTTP: GDELT, RSS, WHO, Ollama, OpenAI"],
                ["beautifulsoup4", "Parsing HTML y extracción de texto"],
            ],
            [3.5 * cm, 13 * cm],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(_p("<b>Nota:</b> pandas NO forma parte del proyecto.", s["body"]))

    # ── 8. JS libs ──
    story.append(_p("8. Librerías JavaScript / Node", s["h1"]))
    story.append(
        _table(
            [
                ["Paquete", "Versión", "Uso"],
                ["next", "^15.1.0", "Framework App Router"],
                ["react / react-dom", "^19.0.0", "UI"],
                ["typescript", "^5.7.2", "Tipado"],
            ],
            [4 * cm, 2.5 * cm, 10 * cm],
        )
    )
    story.append(_p("No se usan: Axios, Redux, Tailwind, shadcn, Chart.js.", s["body"]))

    # ── 9. Flujo ──
    story.append(_p("9. Flujo de verificación (POST /analyze)", s["h1"]))
    flow = [
        "1. Validación del texto (mín. 10 caracteres).",
        "2. Detección de idioma con langdetect.",
        "3. Carga keywords.yaml y trusted_sources.yaml.",
        "4. Extracción de afirmaciones (claim_extractor).",
        "5. Verificación en internet (web_verifier → deep_verifier, RSS, GDELT, DuckDuckGo).",
        "6. Análisis IA opcional (ai_verifier) o local por token overlap.",
        "7. Scoring de fuentes (sources_evaluator, tiers gold/silver/bronze).",
        "8. Modelo 4 pilares (investigation_evaluator).",
        "9. Veredicto final + boost IA (hasta score 98).",
        "10. Respuesta JSON con evidence, claims, recommendations.",
    ]
    for step in flow:
        story.append(_p(step, s["bullet"]))

    # ── 10. Fuentes ──
    story.append(_p("10. Fuentes de datos", s["h1"]))
    story.append(
        _table(
            [
                ["Fuente", "Tipo", "Uso"],
                ["GDELT", "API REST", "Cobertura mediática global"],
                ["WHO / WOAH / CDC / FAO", "RSS + web", "Noticias oficiales"],
                ["Wikipedia", "REST API", "Referencia por enfermedad"],
                ["DuckDuckGo", "HTML", "Búsqueda en dominios oficiales"],
                ["sources_database.yaml", "Local", "150+ fuentes con tier"],
            ],
            [3.5 * cm, 3 * cm, 10 * cm],
        )
    )

    story.append(PageBreak())

    # ── 11. IA ──
    story.append(_p("11. IA, Ollama y análisis local", s["h1"]))
    story.append(_p("Prioridad de proveedores (ai_verifier.py):", s["h2"]))
    for b in [
        "1. OpenAI (OPENAI_API_KEY) → gpt-4o-mini por defecto",
        "2. Anthropic (ANTHROPIC_API_KEY) → claude-3-5-haiku",
        "3. Ollama local (OLLAMA_MODEL) → http://localhost:11434",
        "4. Análisis local sin LLM → solapamiento de tokens",
    ]:
        story.append(_p(b, s["bullet"]))
    story.append(
        _p(
            "Sin API keys la aplicación funciona completamente con verificación profunda + análisis local. "
            "GET /health reporta proveedor y modelo activos.",
            s["body"],
        )
    )

    # ── 12. Extensión ──
    story.append(_p("12. Extensión Chrome", s["h1"]))
    story.append(
        _p(
            "Ubicación: extension/ (Manifest V3). Extrae texto de la pestaña activa "
            "(article o body), envía POST /analyze a localhost:8000 y muestra veredicto y score. "
            "Requiere API en ejecución.",
            s["body"],
        )
    )

    # ── 13. Scripts ──
    story.append(_p("13. Scripts de despliegue local", s["h1"]))
    story.append(
        _table(
            [
                ["Script", "Función"],
                ["iniciar.ps1", "Arranque con ventanas visibles (API + Web)"],
                ["iniciar-background.ps1", "Segundo plano + logs + PIDs"],
                ["detener.ps1", "Detiene puertos 8000 y 3003"],
                ["instalar-inicio.ps1", "Arranque automático Windows"],
                ["tnb-config.ps1", "Puertos: API 8000, Web 3003"],
            ],
            [5 * cm, 11.5 * cm],
        )
    )

    # ── 14. Estructura ──
    story.append(_p("14. Estructura de carpetas", s["h1"]))
    tree = """api/          Backend FastAPI y motor de análisis
web/          Frontend Next.js (app/, components/)
extension/    Extensión Chrome MV3
config/       YAML: keywords, fuentes, enfermedades, pilares
tools/        Scrapers y utilidades
scripts/      PowerShell de arranque
docs/         Documentación técnica
assets/pdfs/  Documentos PDF"""
    for line in tree.split("\n"):
        story.append(_p(line, s["mono"]))

    # ── 15. Endpoints ──
    story.append(_p("15. Endpoints API", s["h1"]))
    story.append(
        _table(
            [
                ["Método", "Ruta", "Descripción"],
                ["GET", "/", "Info básica"],
                ["GET", "/health", "Estado e IA activa"],
                ["GET", "/sources", "Resumen base de fuentes"],
                ["GET", "/source/{domain}", "Detalle de fuente"],
                ["POST", "/analyze", "Analiza texto"],
                ["POST", "/analyze-url", "Analiza URL"],
                ["GET", "/gdelt/search", "Búsqueda GDELT"],
                ["GET", "/gdelt/query-from-text", "Query GDELT desde texto"],
                ["GET", "/news-updates", "Feed de noticias"],
                ["POST", "/news-updates/refresh", "Refresca archivo"],
            ],
            [2 * cm, 5 * cm, 9.5 * cm],
        )
    )
    story.append(_p("Documentación interactiva: http://localhost:8000/docs", s["body"]))

    # ── 16. Equipo ──
    story.append(_p("16. Equipo y colaboración", s["h1"]))
    story.append(
        _p(
            "Repositorio: github.com/JAVGP444/The-NewsBreakers · Licencia MIT (datathon académico). "
            "Colaborar: clonar, rama feature, editar api/ o config/, probar con scripts/iniciar.ps1. "
            "No commitear api/.env con claves.",
            s["body"],
        )
    )

    # ── 17. NO usadas ──
    story.append(_p("17. Tecnologías NO usadas", s["h1"]))
    story.append(
        _table(
            [
                ["Tecnología", "¿Se usa?", "Notas"],
                ["pandas", "NO", "No en requirements ni código"],
                ["SQLite/PostgreSQL", "NO", "Solo JSON + YAML"],
                ["Docker/Kubernetes", "NO", "venv + npm local"],
                ["Tailwind/shadcn", "NO", "CSS propio"],
                ["GraphQL/WebSockets", "NO", "REST + polling HTTP"],
                ["TensorFlow/PyTorch", "NO", "IA vía APIs/Ollama"],
            ],
            [4 * cm, 2 * cm, 10.5 * cm],
        )
    )

    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = _styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2 * cm,
        title="The NewsBreakers - Arquitectura Técnica",
        author="The NewsBreakers",
    )
    doc.build(build_story(styles), onFirstPage=_footer, onLaterPages=_footer)
    print(f"PDF generado: {OUTPUT}")
    print(f"Páginas aproximadas: ver archivo en {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
