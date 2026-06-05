"use client";

import { useState } from "react";
import AnalysisResults, { type AnalysisResult } from "@/components/AnalysisResults";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const EXAMPLES = {
  reliable: "Según WOAH, el brote de influenza aviar H5N1 en aves de corral fue confirmado por laboratorio. Las autoridades sanitarias aplicaron cuarentena veterinaria y sacrificio sanitario según protocolo oficial.",
  suspicious: "¡ALERTA MÁXIMA! Pandemia inminente por gripe aviar — el gobierno oculta la cura milagrosa. NO te vacunes. COMPARTE antes de que borren. Los medios mienten.",
};

export default function Home() {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  async function analyze(endpoint: "analyze" | "analyze-url", body: object) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...body, use_gdelt: true, use_official: true }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail ?? "Error en el análisis");
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error desconocido. ¿Está la API en http://localhost:8000?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="page-bg" />
      <div className="container">
        <header className="header">
          <div className="brand">
            <div className="brand-logo">TNB</div>
            <div>
              <h1>The NewsBreakers</h1>
              <p>Verificador de desinformación · Salud animal</p>
            </div>
          </div>
          <div className="header-badges">
            <span className="pill accent">Datathon 2026</span>
            <span className="pill">10 idiomas</span>
            <span className="pill">GDELT + WOAH/OMS/CDC</span>
          </div>
        </header>

        <section className="hero">
          <h2>¿Es real esta información sobre brotes animales?</h2>
          <p>
            Pega un texto o URL. Nuestro motor analiza idioma, palabras clave veterinarias,
            cobertura global GDELT y titulares oficiales para estimar si es confiable o desinformación.
          </p>
        </section>

        <div className="grid">
          <div className="card">
            <h3>Analizar texto</h3>
            <p className="hint">Noticias, posts, mensajes de WhatsApp, informes…</p>
            <label htmlFor="text">Contenido</label>
            <textarea
              id="text"
              placeholder="Pega aquí el texto a verificar…"
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="actions">
              <button className="btn btn-primary" disabled={loading || text.trim().length < 10} onClick={() => analyze("analyze", { text })}>
                {loading ? <span className="spinner" /> : null}
                {loading ? "Analizando…" : "Verificar texto"}
              </button>
              <button className="btn btn-secondary" type="button" onClick={() => setText(EXAMPLES.reliable)}>Ej. confiable</button>
              <button className="btn btn-secondary" type="button" onClick={() => setText(EXAMPLES.suspicious)}>Ej. sospechoso</button>
            </div>
          </div>

          <div className="card">
            <h3>Analizar desde URL</h3>
            <p className="hint">Extraemos el artículo y aplicamos el mismo análisis</p>
            <label htmlFor="url">Enlace</label>
            <input id="url" type="url" placeholder="https://www.woah.org/…" value={url} onChange={(e) => setUrl(e.target.value)} />
            <div className="actions">
              <button className="btn btn-secondary" disabled={loading || !url.startsWith("http")} onClick={() => analyze("analyze-url", { url })}>
                Verificar URL
              </button>
            </div>
          </div>
        </div>

        {error && <div className="error-box">{error}</div>}
        {result && <AnalysisResults result={result} />}

        <footer className="footer">
          The NewsBreakers · Datathon · No sustituye verificación humana profesional · IFCN / WOAH / GDELT
        </footer>
      </div>
    </>
  );
}
