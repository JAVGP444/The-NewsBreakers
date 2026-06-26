#!/usr/bin/env python3
"""Genera PDF de especificaciones técnicas completas de The NewsBreakers."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(r"C:\Users\javie\OneDrive\Escritorio\The-NewsBreakers-Especificaciones.pdf")
FOOTER_DATE = "Junio 2026"


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, f"The NewsBreakers — Especificaciones Técnicas · {FOOTER_DATE}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "DocTitle",
            parent=base["Title"],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=colors.HexColor("#0a2540"),
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base["Normal"],
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=5,
            textColor=colors.HexColor("#425466"),
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontSize=15,
            leading=19,
            spaceBefore=14,
            spaceAfter=7,
            textColor=colors.HexColor("#0a2540"),
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=5,
            textColor=colors.HexColor("#1a3a5c"),
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=9.5,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            leftIndent=12,
            spaceAfter=2,
        ),
        "toc": ParagraphStyle(
            "TOC",
            parent=base["Normal"],
            fontSize=9.5,
            leading=15,
            leftIndent=6,
        ),
        "mono": ParagraphStyle(
            "Mono",
            parent=base["Code"],
            fontSize=7.5,
            leading=9.5,
            fontName="Courier",
            spaceAfter=3,
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
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d0d7de")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fa")]),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def build_story(s: dict) -> list:
    story: list = []

    # Portada
    story.append(Spacer(1, 3.5 * cm))
    story.append(_p("The NewsBreakers", s["title"]))
    story.append(_p("Especificaciones Técnicas del Proyecto", s["title"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(_p("Verificador de desinformación en salud animal y brotes epizoóticos", s["subtitle"]))
    story.append(_p("Documento integral: arquitectura, stack, UI, colaboración y despliegue", s["subtitle"]))
    story.append(Spacer(1, 1.2 * cm))
    story.append(_p(f"Versión 1.1.0 · {FOOTER_DATE}", s["subtitle"]))
    story.append(_p("Repositorio: github.com/JAVGP444/The-NewsBreakers · Licencia MIT", s["subtitle"]))
    story.append(PageBreak())

    # Índice
    story.append(_p("Tabla de contenidos", s["h1"]))
    for i, item in enumerate(
        [
            "1. Resumen ejecutivo",
            "2. Lenguajes de programación",
            "3. Código abierto y licencia",
            "4. Arquitectura del sistema",
            "5. Diseño de página e interfaz (UI)",
            "6. Frontend: Next.js, React, TypeScript",
            "7. Backend: FastAPI y estructura API",
            "8. Dependencias Python y Node",
            "9. Uso de pandas",
            "10. Bases de datos y almacenamiento",
            "11. Integración IA / Ollama",
            "12. Archivos de configuración (YAML)",
            "13. Scripts PowerShell",
            "14. Colaboración GitHub (.github/)",
            "15. Flujo de trabajo en equipo",
            "16. Endpoints API",
            "17. Tecnologías no utilizadas",
        ],
        1,
    ):
        story.append(_p(f"{item}", s["toc"]))
    story.append(PageBreak())

    # 1. Resumen
    story.append(_p("1. Resumen ejecutivo", s["h1"]))
    story.append(
        _p(
            "<b>The NewsBreakers</b> automatiza un primer filtro de verificación de noticias sobre "
            "salud animal, brotes epizoóticos y zoónosis. Analiza texto o URL y devuelve veredicto "
            "explicable (verified, false, unverified, uncertain) con score 0–100, evidencia enlazada, "
            "modelo de 4 pilares y recomendaciones. Soporta hasta 10 idiomas.",
            s["body"],
        )
    )
    story.append(
        _p(
            "Componentes: frontend Next.js 15 (puerto <b>3003</b>), API FastAPI (puerto <b>8000</b>), "
            "motor modular Python, extensión Chrome MV3, configuración YAML y persistencia JSON. "
            "Repositorio público en GitHub bajo licencia MIT (proyecto académico / datathon).",
            s["body"],
        )
    )

    # 2. Lenguajes
    story.append(_p("2. Lenguajes de programación", s["h1"]))
    story.append(
        _table(
            [
                ["Lenguaje", "Ubicación", "Uso principal"],
                ["Python 3.12+", "api/, tools/, scripts aux.", "Backend, motor de análisis, scrapers"],
                ["TypeScript", "web/", "Frontend Next.js con tipado estático"],
                ["JavaScript", "extension/", "Popup de extensión Chrome MV3"],
                ["CSS", "web/app/", "Tema visual (globals.css, dashboard.css)"],
                ["YAML", "config/", "Keywords, fuentes, enfermedades, modelo de pilares"],
                ["PowerShell", "scripts/", "Arranque y despliegue local en Windows"],
                ["Markdown", "docs/, .github/", "Documentación y plantillas GitHub"],
            ],
            [2.8 * cm, 4.5 * cm, 9.2 * cm],
        )
    )

    # 3. Open source
    story.append(_p("3. Código abierto y licencia", s["h1"]))
    story.append(
        _p(
            "El proyecto es <b>open source</b> y está publicado en GitHub: "
            "<b>https://github.com/JAVGP444/The-NewsBreakers</b>. Licencia <b>MIT</b> (README.md): "
            "uso, modificación y distribución permitidos con atribución. Proyecto académico orientado "
            "a datathon y portfolio. No incluye secretos en el repositorio: claves API van en "
            "api/.env (gitignored).",
            s["body"],
        )
    )

    # 4. Arquitectura
    story.append(_p("4. Arquitectura del sistema", s["h1"]))
    story.append(_p("Tipo: arquitectura modular en pipeline", s["h2"]))
    story.append(
        _p(
            "No es un flujo lineal monolítico: el orquestador <b>analyzer.py</b> coordina módulos "
            "independientes (extracción, verificación web, IA, evaluación de pilares, fuentes). "
            "Cada módulo tiene responsabilidad única y puede evolucionar por separado. La configuración "
            "externa (YAML) desacopla reglas de negocio del código. Flujo de datos: recepción → "
            "detección idioma → extracción afirmaciones → búsqueda evidencia → scoring → veredicto.",
            s["body"],
        )
    )
    arch = """Usuario → Web (Next.js :3003) ──→ API (FastAPI :8000) ──→ analyzer.py
                                              ├── claim_extractor.py
                                              ├── web_verifier.py + deep_verifier.py
                                              ├── gdelt_fetcher.py + trusted_search.py
                                              ├── ai_verifier.py (Ollama/OpenAI/local)
                                              ├── investigation_evaluator.py (4 pilares)
                                              └── sources_evaluator.py (150+ fuentes)
Extensión Chrome ──→ POST /analyze          news_aggregator → news_archive.json"""
    for line in arch.split("\n"):
        story.append(_p(line, s["mono"]))

    story.append(PageBreak())

    # 5. UI
    story.append(_p("5. Diseño de página e interfaz (UI)", s["h1"]))
    story.append(_p("Estructura y componentes", s["h2"]))
    story.append(
        _table(
            [
                ["Archivo", "Función"],
                ["web/app/layout.tsx", "Layout raíz, metadatos SEO, importación CSS"],
                ["web/app/page.tsx", "Dashboard: verificador, feed noticias, historial"],
                ["web/app/globals.css", "Variables CSS, tipografía, tokens de color"],
                ["web/app/dashboard.css", "Grid, cards, chips, layout del dashboard"],
                ["web/components/AnalysisResults.tsx", "Veredicto, pilares, evidencia, IA"],
                ["web/components/dashboard/NewsCardItem.tsx", "Tarjeta de noticia del feed"],
                ["web/components/dashboard/VerificationHistory.tsx", "Historial en localStorage"],
            ],
            [5.5 * cm, 11 * cm],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(_p("Tema visual", s["h2"]))
    story.append(
        _p(
            "Dashboard profesional con <b>paleta oscura</b>: fondo #060d18, superficies #111c2e, "
            "acento azul #2563eb. Colores semánticos: verde (#10b981) confiable, ámbar (#f59e0b) "
            "dudoso, rojo (#ef4444) sospechoso. Tipografía Inter/Segoe UI. Sin Tailwind ni kits UI "
            "externos — CSS propio modular. Puerto web: <b>3003</b>. Variable NEXT_PUBLIC_API_URL "
            "(default http://localhost:8000).",
            s["body"],
        )
    )
    story.append(_p("Funcionalidades UI", s["h2"]))
    for b in [
        "Verificador dual: texto (POST /analyze) o URL (POST /analyze-url).",
        "Ejemplos precargados: noticia confiable, desmentido, texto sospechoso.",
        "Feed de noticias con pestañas trending/archivo/todas; filtros WOAH, OMS, CDC, FAO, GDELT.",
        "Polling cada 10 min a /news-updates; chips de enfermedades con nivel de riesgo.",
        "Historial local de verificaciones (localStorage, no se envía al servidor).",
    ]:
        story.append(_p(f"• {b}", s["bullet"]))

    # 6. Frontend
    story.append(_p("6. Frontend: Next.js, React, TypeScript", s["h1"]))
    story.append(
        _table(
            [
                ["Tecnología", "Versión", "Uso"],
                ["Next.js", "^15.1.0", "App Router, SSR/CSR, routing"],
                ["React", "^19.0.0", "UI declarativa"],
                ["React DOM", "^19.0.0", "Renderizado en DOM"],
                ["TypeScript", "^5.7.2", "Tipado estático"],
                ["CSS propio", "—", "globals.css + dashboard.css"],
            ],
            [3.2 * cm, 2.3 * cm, 11 * cm],
        )
    )
    story.append(_p("Scripts npm: dev (puerto 3003), build, start, clean, rebuild.", s["body"]))

    # 7. Backend
    story.append(_p("7. Backend: FastAPI y estructura API", s["h1"]))
    story.append(
        _table(
            [
                ["Módulo", "Responsabilidad"],
                ["main.py", "Endpoints, CORS, lifespan, background news refresh"],
                ["analyzer.py", "Orquestador principal del análisis"],
                ["claim_extractor.py", "Extracción de afirmaciones estructuradas"],
                ["web_verifier.py", "Búsqueda internet: GDELT, WHO, DuckDuckGo, RSS"],
                ["deep_verifier.py", "URLs en texto + news_archive.json"],
                ["ai_verifier.py", "OpenAI / Anthropic / Ollama / análisis local"],
                ["investigation_evaluator.py", "Modelo 4 pilares + reglas R1–R9"],
                ["sources_evaluator.py", "150+ fuentes gold/silver/bronze"],
                ["news_aggregator.py", "RSS + GDELT → news_archive.json"],
                ["gdelt_fetcher.py", "Cliente GDELT Doc API"],
                ["disease_catalog.py", "Catálogo enfermedades desde YAML"],
                ["url_fetcher.py", "Extracción texto de URLs (BeautifulSoup)"],
            ],
            [4.2 * cm, 12.3 * cm],
        )
    )

    story.append(PageBreak())

    # 8. Dependencias
    story.append(_p("8. Dependencias Python y Node", s["h1"]))
    story.append(_p("Python (api/requirements.txt)", s["h2"]))
    story.append(
        _table(
            [
                ["Librería", "Versión", "Uso"],
                ["fastapi", "≥0.115.6", "API REST, OpenAPI"],
                ["uvicorn[standard]", "≥0.34.0", "Servidor ASGI"],
                ["pydantic", "≥2.11.0", "Validación de modelos"],
                ["langdetect", "1.0.9", "Detección de idioma"],
                ["pyyaml", "≥6.0.2", "Lectura config/*.yaml"],
                ["httpx", "≥0.28.1", "HTTP: GDELT, RSS, Ollama, LLMs"],
                ["beautifulsoup4", "≥4.12.3", "Parsing HTML"],
            ],
            [3.2 * cm, 2.3 * cm, 11 * cm],
        )
    )
    story.append(_p("Node (web/package.json)", s["h2"]))
    story.append(
        _table(
            [
                ["Paquete", "Versión", "Uso"],
                ["next", "^15.1.0", "Framework"],
                ["react / react-dom", "^19.0.0", "UI"],
                ["typescript", "^5.7.2", "Tipado (dev)"],
                ["@types/*", "^19–22", "Tipos TypeScript (dev)"],
            ],
            [3.5 * cm, 2.5 * cm, 10.5 * cm],
        )
    )
    story.append(_p("No se usan: Axios, Redux, Tailwind, shadcn, Chart.js.", s["body"]))

    # 9. pandas
    story.append(_p("9. Uso de pandas", s["h1"]))
    story.append(
        _p(
            "<b>pandas NO se utiliza en este proyecto.</b> No aparece en api/requirements.txt, "
            "no hay import pandas en ningún archivo del código fuente. El procesamiento de datos "
            "se realiza con estructuras nativas de Python (dict, list), JSON y YAML. "
            "numpy tampoco está incluido.",
            s["body"],
        )
    )

    # 10. Bases de datos
    story.append(_p("10. Bases de datos y almacenamiento", s["h1"]))
    story.append(
        _table(
            [
                ["Almacén", "Ubicación", "Propósito"],
                ["JSON noticias", "api/news_archive.json", "Histórico validado (máx. 500 ítems)"],
                ["JSON legacy", "api/news_updates.json", "Formato anterior; migración automática"],
                ["YAML", "config/*.yaml", "Keywords, fuentes, enfermedades, pilares"],
                ["localStorage", "Navegador", "Historial verificaciones usuario"],
                ["GDELT", "API externa", "Cobertura mediática global (no BD local)"],
                ["Logs", "logs/*.log", "Servicios background (gitignored)"],
            ],
            [2.8 * cm, 4.8 * cm, 9 * cm],
        )
    )
    story.append(
        _p(
            "<b>No hay SQL en producción:</b> SQLite, PostgreSQL, MySQL, MongoDB y Redis no están "
            "implementados. La carpeta data/databases/ está documentada como uso futuro.",
            s["body"],
        )
    )

    # 11. IA
    story.append(_p("11. Integración IA / Ollama", s["h1"]))
    for b in [
        "1. OpenAI (OPENAI_API_KEY) → gpt-4o-mini por defecto",
        "2. Anthropic (ANTHROPIC_API_KEY) → claude-3-5-haiku",
        "3. Ollama local (OLLAMA_MODEL) → http://localhost:11434",
        "4. Análisis local sin LLM → solapamiento de tokens (funciona sin claves)",
    ]:
        story.append(_p(b, s["bullet"]))
    story.append(
        _p(
            "Variables en api/.env (ver api/.env.example). GET /health reporta proveedor y modelo activos. "
            "Sin API keys la app funciona con verificación profunda + análisis local.",
            s["body"],
        )
    )

    story.append(PageBreak())

    # 12. Config YAML
    story.append(_p("12. Archivos de configuración (YAML)", s["h1"]))
    story.append(
        _table(
            [
                ["Archivo", "Contenido"],
                ["config/keywords.yaml", "Palabras clave topic/alarm/trust por idioma"],
                ["config/trusted_sources.yaml", "Dominios oficiales y fact-checkers"],
                ["config/sources_database.yaml", "150+ fuentes con tier y confianza"],
                ["config/diseases_catalog.yaml", "Enfermedades, regex, queries GDELT"],
                ["config/investigation_model.yaml", "Modelo 4 pilares y reglas R1–R9"],
                ["config/indicators.yaml", "Indicadores de análisis"],
            ],
            [5.5 * cm, 11 * cm],
        )
    )

    # 13. Scripts
    story.append(_p("13. Scripts PowerShell (scripts/)", s["h1"]))
    story.append(
        _table(
            [
                ["Script", "Función"],
                ["tnb-config.ps1", "Puertos compartidos: API 8000, Web 3003"],
                ["iniciar.ps1", "Arranque con ventanas visibles (API + Web)"],
                ["iniciar-background.ps1", "Segundo plano + logs + PIDs en .run/"],
                ["detener.ps1", "Detiene procesos en puertos 8000 y 3003"],
                ["instalar-inicio.ps1", "Arranque automático al iniciar Windows"],
                ["desinstalar-inicio.ps1", "Elimina arranque automático"],
            ],
            [5 * cm, 11.5 * cm],
        )
    )

    # 14. GitHub
    story.append(_p("14. Colaboración GitHub (.github/)", s["h1"]))
    story.append(
        _table(
            [
                ["Archivo", "Propósito"],
                ["CONTRIBUTING.md", "Guía de contribución, ramas, commits, PRs"],
                ["CODEOWNERS", "Revisores automáticos por carpeta (@JAVGP444)"],
                ["pull_request_template.md", "Checklist al abrir PR"],
                ["ISSUE_TEMPLATE/bug_report.md", "Plantilla reporte de bug"],
                ["ISSUE_TEMPLATE/feature_request.md", "Plantilla solicitud de feature"],
                ["workflows/ci.yml", "CI: compileall Python + build Next.js"],
            ],
            [5.5 * cm, 11 * cm],
        )
    )
    story.append(
        _p(
            "CI se ejecuta en push/PR a master, develop y main. Jobs: API sintaxis Python, Web build Next.js. "
            "Sin secretos en el workflow.",
            s["body"],
        )
    )

    # 15. Team workflow
    story.append(_p("15. Flujo de trabajo en equipo", s["h1"]))
    story.append(
        _p(
            "Documento completo: docs/TEAM_WORKFLOW.md. Modelo de ramas: "
            "<b>feature/* → develop → master</b>. Rama principal actual: master. "
            "develop como rama de integración diaria. Alternativas: GitHub Codespaces, VS Code Live Share. "
            "Protección de ramas recomendada en Settings → Branches. Roles: Maintainer, Backend, Frontend, Docs/demo.",
            s["body"],
        )
    )
    for b in [
        "Tomar tarea vía issue → rama feature → commits pequeños → PR a develop.",
        "Code review: al menos 1 aprobación; CI verde antes de merge.",
        "Release/demo: PR develop → master con tag v1.0-demo opcional.",
        "No commitear api/.env ni claves; usar .env.example como plantilla.",
    ]:
        story.append(_p(f"• {b}", s["bullet"]))

    # 16. Endpoints
    story.append(_p("16. Endpoints API", s["h1"]))
    story.append(
        _table(
            [
                ["Método", "Ruta", "Descripción"],
                ["GET", "/", "Info básica de la API"],
                ["GET", "/health", "Estado, versión, IA activa"],
                ["GET", "/sources", "Resumen base de fuentes"],
                ["GET", "/source/{domain}", "Detalle de fuente por dominio"],
                ["POST", "/analyze", "Analiza texto (min. 10 chars)"],
                ["POST", "/analyze-url", "Analiza URL (extrae texto)"],
                ["GET", "/gdelt/search", "Búsqueda directa GDELT"],
                ["GET", "/gdelt/query-from-text", "Query GDELT desde texto"],
                ["GET", "/news-updates", "Feed de noticias validadas"],
                ["POST", "/news-updates/refresh", "Fuerza refresco del archivo"],
            ],
            [1.8 * cm, 4.8 * cm, 10 * cm],
        )
    )
    story.append(_p("Documentación interactiva: http://localhost:8000/docs", s["body"]))

    # 17. No usadas
    story.append(_p("17. Tecnologías no utilizadas", s["h1"]))
    story.append(
        _table(
            [
                ["Tecnología", "¿Se usa?", "Notas"],
                ["pandas / numpy", "NO", "Solo dict/list/JSON/YAML"],
                ["SQLite / PostgreSQL", "NO", "Persistencia JSON + YAML"],
                ["Docker / Kubernetes", "NO", "venv + npm local"],
                ["Tailwind / shadcn", "NO", "CSS propio"],
                ["GraphQL / WebSockets", "NO", "REST + polling HTTP"],
                ["TensorFlow / PyTorch", "NO", "IA vía APIs/Ollama"],
                ["Redis / Celery", "NO", "asyncio + threading"],
            ],
            [3.8 * cm, 1.8 * cm, 11 * cm],
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
        title="The NewsBreakers - Especificaciones Técnicas",
        author="The NewsBreakers",
    )
    doc.build(build_story(styles), onFirstPage=_footer, onLaterPages=_footer)
    size = OUTPUT.stat().st_size
    print(f"PDF generado: {OUTPUT}")
    print(f"Tamaño: {size:,} bytes ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
