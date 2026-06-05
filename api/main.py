"""API The NewsBreakers — verificación de desinformación en salud animal."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from analyzer import analyze_text
from gdelt_fetcher import search_animal_health, build_query_from_text
from url_fetcher import extract_text_from_url

app = FastAPI(
    title="The NewsBreakers API",
    description="Verificación multilingüe de información sobre salud animal y brotes",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10)
    use_gdelt: bool = True
    use_official: bool = True


class AnalyzeUrlRequest(BaseModel):
    url: str
    use_gdelt: bool = True
    use_official: bool = True


@app.get("/health")
def health():
    return {
        "status": "ok",
        "team": "The NewsBreakers",
        "version": "1.0.0",
        "features": ["multilingual", "gdelt", "official_feeds", "keyword_classifier"],
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        return analyze_text(request.text, request.use_gdelt, request.use_official)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/analyze-url")
def analyze_url(request: AnalyzeUrlRequest):
    try:
        text, meta = extract_text_from_url(request.url)
        result = analyze_text(text, request.use_gdelt, request.use_official)
        result["source_url"] = request.url
        result["extraction"] = meta
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/gdelt/search")
def gdelt_search(q: str = Query(default="avian flu OR H5N1 OR gripe aviar"), limit: int = 8):
    articles = search_animal_health(query=q, max_records=min(limit, 20))
    return {"query": q, "count": len(articles), "articles": articles}


@app.get("/gdelt/query-from-text")
def gdelt_query_preview(text: str = Query(..., min_length=10)):
    return {"query": build_query_from_text(text)}
