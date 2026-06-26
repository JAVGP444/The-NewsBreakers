# The NewsBreakers

**Verificador profesional de desinformación en salud animal y brotes epizoóticos.**

## Qué hace
- Detecta fake news en texto y URL.
- Soporta hasta 10 idiomas.
- Contrasta con fuentes oficiales WOAH/WHO/CDC, GDELT y verificadores de hechos.
- Genera veredictos explicables con score, indicadores y recomendaciones.

## Por qué es profesional
- Arquitectura clara: frontend, API y motor de análisis.
- Resultados explicables para jurado y stakeholders.
- Documentación lista: guías, demo, materiales PDF y notas técnicas.
- Extensión Chrome que reutiliza la misma API.

## Arquitectura

```text
Usuario → Web (Next.js) ──→ API (FastAPI) ──→ Motor de análisis
                                    ├── GDELT (cobertura global)
                                    ├── Feeds oficiales (WOAH/WHO/CDC)
                                    └── Clasificador por keywords
Extensión Chrome ──────────→ misma API
```

## Inicio rápido

### Backend

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```powershell
cd web
npm install
npm run dev
```

Accede a:

- `http://localhost:3003` (app web). API: `http://localhost:8000/docs`
- `http://localhost:8000/docs`

## Estructura del proyecto

| Carpeta | Uso |
|---------|-----|
| `api/` | Backend, FastAPI y motor de análisis |
| `web/` | Interfaz de usuario de demostración |
| `extension/` | Extensión Chrome |
| `config/` | Keywords, indicadores y fuentes confiables |
| `tools/` | Scrapers y utilidades |
| `assets/images` | Logos y capturas |
| `assets/pdfs` | Documentación profesional |
| `assets/excels` | Datasets y tablas |
| `data/raw` | Exportaciones GDELT y feeds brutos |
| `data/databases` | SQLite y CSV de trabajo |

## Trabajo en equipo

Este repo está preparado para colaboración en GitHub (datathon / portfolio):

- **[docs/TEAM_WORKFLOW.md](docs/TEAM_WORKFLOW.md)** — Flujo de ramas (`develop`, `feature/*`), Codespaces, Live Share y tips de demo.
- **[.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)** — Cómo abrir PRs, revisar código y convenciones de commits.
- **Plantillas** — Issues (bug / feature) y checklist de Pull Request en `.github/`.

Modelo recomendado: `feature/*` → `develop` → `master`, con revisiones y CI automático en cada PR.

## Documentación clave
- `docs/DEMO.md` — Guía de presentación para jurado.
- `docs/TEAM_WORKFLOW.md` — Colaboración en equipo y GitHub.
- `docs/methodology.md` — Metodología del proyecto.
- `docs/identificacion-fake-news.md` — Guía práctica para detectar fake news.
- `assets/pdfs/Identificacion-noticias-falsas.pdf` — Documento técnico listo.
- `api/README.md` — Guía de backend.
- `web/README.md` — Guía de frontend.

## Fuentes recomendadas para verificación
1. WAHIS
2. WOAH
3. CDC
4. WHO
5. FAO
6. ProMED
7. PubMed
8. Scopus
9. Web of Science
10. Revistas científicas especializadas

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/analyze` | Analiza texto |
| POST | `/analyze-url` | Analiza URL |
| GET | `/gdelt/search` | Búsqueda GDELT |
| GET | `/gdelt/query-from-text` | Genera consulta GDELT |
| GET | `/health` | Estado del servicio |

## Clonar

```bash
git clone https://github.com/JAVGP444/The-NewsBreakers.git
cd The-NewsBreakers
```

## Licencia

MIT — proyecto académico / datathon.
