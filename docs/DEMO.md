# Guía de demo — Jurado del datathon

## Antes de la presentación (5 min)

```powershell
# Terminal 1 — API
cd api
.venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2 — Web
cd web
npm run dev

# Opcional — precargar feeds oficiales
cd ..
api\.venv\Scripts\python.exe tools\official_scraper.py
```

## Flujo de demo (3 min)

1. Abrir **http://localhost:3000**
2. Clic en **「Ej. confiable」** → **Verificar texto**
   - Veredicto verde, score alto, GDELT y fuentes oficiales
3. Clic en **「Ej. sospechoso」** → **Verificar texto**
   - Veredicto rojo, señales de alarma, penalizaciones visibles
4. Pegar URL de noticia real (WOAH o medio sensacionalista) → **Verificar URL**
5. Mostrar **desglose del score** y artículos GDELT relacionados

## Extensión Chrome (opcional)

1. `chrome://extensions` → Modo desarrollador → **Cargar descomprimida**
2. Carpeta: `extension/`
3. Abrir artículo → clic icono TNB → **Verificar esta página**

## Mensaje clave para el jurado

> "Contrastamos cada texto con **tres capas**: palabras clave veterinarias multilingües, **cobertura global GDELT** y **titulares oficiales WOAH/OMS/CDC**, generando un score explicable y recomendaciones accionables."
