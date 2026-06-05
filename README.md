# The NewsBreakers

**Verificador profesional de desinformación sobre salud animal y brotes epizoóticos.**

Proyecto de datathon: analiza texto o URLs en **10 idiomas**, contrasta con **GDELT**, **WOAH**, **OMS** y **CDC**, y devuelve un veredicto explicable con indicadores y recomendaciones.

## Equipo

**The NewsBreakers**

## Ubicación

```
C:\Users\javie\OneDrive\Escritorio\the-newsbreakers
```

## Arquitectura

```
Usuario → Web (Next.js) ──→ API (FastAPI) ──→ Motor de análisis
                                    ├── GDELT (cobertura global)
                                    ├── Feeds oficiales (WOAH/OMS/CDC)
                                    └── Clasificador por keywords
Extensión Chrome ──────────→ misma API
```

## Inicio rápido

### API

```powershell
cd api
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Web

```powershell
cd web
npm install
npm run dev
```

→ http://localhost:3000 · API docs: http://localhost:8000/docs

### Feeds oficiales

```powershell
api\.venv\Scripts\python.exe tools\official_scraper.py
```

## Estructura

| Carpeta | Uso |
|---------|-----|
| `api/` | Backend y motor de análisis |
| `web/` | Página de consultoría (demo jurado) |
| `extension/` | Extensión Chrome |
| `config/` | Keywords, indicadores, fuentes |
| `tools/` | Scrapers y utilidades |
| `assets/images` | Logo, capturas |
| `assets/pdfs` | Brief datathon |
| `assets/excels` | Datasets Excel |
| `data/raw` | GDELT exports, feeds JSON |
| `data/databases` | SQLite / CSV grandes |

## API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/analyze` | Analiza texto |
| POST | `/analyze-url` | Analiza URL |
| GET | `/gdelt/search` | Búsqueda GDELT |
| GET | `/health` | Estado |

## Demo

Ver [docs/DEMO.md](docs/DEMO.md)

## Clonar (equipo)

```bash
git clone https://github.com/JAVGP444/The-NewsBreakers.git
cd The-NewsBreakers
```

## Licencia

MIT — proyecto académico / datathon.
