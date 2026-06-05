type Article = { title: string; url: string; domain?: string; seendate?: string };
type OfficialMatch = { source: string; title: string; link: string };

export type AnalysisResult = {
  score: number;
  verdict: "reliable" | "uncertain" | "suspicious";
  verdict_es: string;
  score_breakdown: { label: string; delta: number }[];
  indicators: {
    language: string;
    topic_matches: string[];
    alarm_matches: string[];
    trust_matches: string[];
    official_links: string[];
    fact_check_links: string[];
    alarm_density: number;
    sensationalism_flags: number;
    laboratory_confirmed: boolean;
    gdelt_status?: string;
    gdelt_articles_found?: number;
    official_feed_alignment?: boolean;
    word_count: number;
  };
  recommendations: string[];
  gdelt: {
    status: string;
    query?: string;
    articles_found: number;
    trusted_in_results: boolean;
    related_articles: Article[];
  };
  official_sources: {
    aligned: boolean;
    matches: OfficialMatch[];
    feed_count: number;
  };
};

function gdeltStatusLabel(status: string) {
  const map: Record<string, string> = {
    corroborated: "Corroborado globalmente",
    partial_coverage: "Cobertura parcial",
    unverified_claim: "Afirmación sin verificar",
    alarm_without_coverage: "Alarma sin cobertura",
    no_data: "Sin datos GDELT",
    skipped: "No consultado",
  };
  return map[status] ?? status;
}

export default function AnalysisResults({ result }: { result: AnalysisResult }) {
  const { indicators: ind } = result;

  return (
    <div className="results">
      <div className={`verdict-banner ${result.verdict}`}>
        <div>
          <h3>{result.verdict_es}</h3>
          <p style={{ color: "var(--muted)", fontSize: "0.9rem", marginTop: "0.35rem" }}>
            Idioma: <strong>{ind.language.toUpperCase()}</strong> · {ind.word_count} palabras
            {ind.laboratory_confirmed && " · Caso confirmado por laboratorio"}
          </p>
        </div>
        <div className="score-ring">
          <div className="value">{result.score}</div>
          <div className="label">/ 100 confiabilidad</div>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric">
          <div className="name">GDELT</div>
          <div className="val">{gdeltStatusLabel(result.gdelt.status)}</div>
          <div style={{ fontSize: "0.75rem", color: "var(--muted)", marginTop: "0.25rem" }}>
            {result.gdelt.articles_found} artículos · {result.gdelt.trusted_in_results ? "con medios oficiales" : "sin fuentes top"}
          </div>
        </div>
        <div className="metric">
          <div className="name">Fuentes oficiales</div>
          <div className="val">{result.official_sources.aligned ? "Alineado" : "Sin coincidencia"}</div>
          <div style={{ fontSize: "0.75rem", color: "var(--muted)", marginTop: "0.25rem" }}>
            {result.official_sources.feed_count} titulares WOAH/OMS/CDC
          </div>
        </div>
        <div className="metric">
          <div className="name">Densidad alarma</div>
          <div className="val">{(ind.alarm_density * 100).toFixed(1)}%</div>
        </div>
        <div className="metric">
          <div className="name">Sensacionalismo</div>
          <div className="val">{ind.sensationalism_flags} / 4 flags</div>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Indicadores detectados</h3>
          <p className="hint">Clasificación por palabras clave veterinarias multilingües</p>

          {ind.topic_matches.length > 0 && (
            <>
              <div className="section-title">Tema salud animal</div>
              <ul className="tags topic">{ind.topic_matches.map((t) => <li key={t}>{t}</li>)}</ul>
            </>
          )}
          {ind.trust_matches.length > 0 && (
            <>
              <div className="section-title">Señales de confianza</div>
              <ul className="tags trust">{ind.trust_matches.map((t) => <li key={t}>{t}</li>)}</ul>
            </>
          )}
          {ind.alarm_matches.length > 0 && (
            <>
              <div className="section-title">Señales de alarma</div>
              <ul className="tags alarm">{ind.alarm_matches.map((t) => <li key={t}>{t}</li>)}</ul>
            </>
          )}
        </div>

        <div className="card">
          <h3>Desglose del score</h3>
          <p className="hint">Pesos calibrados para el datathon</p>
          <ul className="breakdown-list">
            {result.score_breakdown.map((b) => (
              <li key={b.label}>
                <span>{b.label}</span>
                <span className={b.delta >= 0 ? "pos" : "neg"}>
                  {b.delta > 0 ? "+" : ""}{b.delta}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {result.gdelt.related_articles.length > 0 && (
        <div className="card" style={{ marginTop: "1.25rem" }}>
          <h3>Cobertura GDELT relacionada</h3>
          <p className="hint">Noticias globales recientes sobre el mismo tema</p>
          <ul className="article-list">
            {result.gdelt.related_articles.map((a) => (
              <li key={a.url}>
                <a href={a.url} target="_blank" rel="noopener noreferrer">{a.title}</a>
                <div className="meta">{a.domain} · {a.seendate}</div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.official_sources.matches.length > 0 && (
        <div className="card" style={{ marginTop: "1.25rem" }}>
          <h3>Titulares oficiales relacionados</h3>
          <ul className="article-list">
            {result.official_sources.matches.map((m) => (
              <li key={m.link + m.title}>
                <strong>[{m.source}]</strong> {m.title}
                {m.link && (
                  <> — <a href={m.link} target="_blank" rel="noopener noreferrer">ver</a></>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.recommendations.length > 0 && (
        <div className="card" style={{ marginTop: "1.25rem" }}>
          <h3>Recomendaciones</h3>
          <ul className="rec-list">
            {result.recommendations.map((r) => <li key={r}>{r}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
