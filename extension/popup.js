const API = "http://localhost:8000";

document.getElementById("verify").addEventListener("click", async () => {
  const btn = document.getElementById("verify");
  const out = document.getElementById("result");
  btn.disabled = true;
  out.innerHTML = "Analizando…";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const [{ result: pageText }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        const article = document.querySelector("article");
        const text = article ? article.innerText : document.body.innerText;
        return (document.title + "\n\n" + text).slice(0, 12000);
      },
    });

    const res = await fetch(`${API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: pageText, use_gdelt: true, use_official: true }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Error API");

    out.innerHTML = `
      <div class="verdict ${data.verdict}">${data.verdict_es}</div>
      <div>Score: <strong>${data.score}/100</strong> · ${data.indicators.language.toUpperCase()}</div>
      <div style="margin-top:6px;color:#8ba3c7">GDELT: ${data.gdelt.articles_found} artículos</div>
      <ul>${(data.recommendations || []).slice(0, 3).map((r) => `<li>${r}</li>`).join("")}</ul>
    `;
  } catch (e) {
    out.innerHTML = `<div class="err">${e.message}. ¿API en localhost:8000?</div>`;
  } finally {
    btn.disabled = false;
  }
});
