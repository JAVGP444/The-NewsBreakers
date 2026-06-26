# Guía de contribución — The NewsBreakers

Gracias por colaborar en este proyecto de portfolio / datathon. Esta guía resume cómo trabajar en equipo sin pisarnos el trabajo.

## Antes de empezar

1. Lee [docs/TEAM_WORKFLOW.md](../docs/TEAM_WORKFLOW.md) para el flujo completo del equipo.
2. Clona el repositorio y configura el entorno local (ver [README.md](../README.md)).
3. Copia las variables de ejemplo si las necesitas:
   - `api/.env.example` → `api/.env` (no subas `.env` a Git).
   - `web/.env.example` → `web/.env.local` (opcional).

## Modelo de ramas

| Rama | Uso |
|------|-----|
| `master` | Código estable listo para demo / entrega. Solo entra vía PR revisado. |
| `develop` | Integración diaria del equipo. Base para nuevas features. |
| `feature/*` | Una rama por tarea (ej. `feature/dashboard-filtros`). |
| `fix/*` | Correcciones puntuales (ej. `fix/gdelt-timeout`). |

### Flujo recomendado

```text
feature/mi-tarea  →  develop  →  master
                      ↑              ↑
                   PR + review    PR + review
```

1. Actualiza tu copia local:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Crea tu rama de trabajo:
   ```bash
   git checkout -b feature/nombre-corto
   ```
3. Haz commits pequeños y descriptivos (en español o inglés, pero consistente en el PR).
4. Sube la rama y abre un **Pull Request** hacia `develop`.
5. Pide revisión a al menos un compañero antes de mergear.
6. Cuando `develop` esté estable para la entrega, abrid un PR de `develop` → `master`.

> **Nota:** La rama principal actual del repo es `master`. Si el equipo prefiere `main`, renómbrala en GitHub (Settings → Branches) y actualiza esta guía.

## Commits

- Un commit = un cambio lógico (fix, feature, docs).
- Mensaje claro: _qué_ y _por qué_, no solo _qué archivos_.

Ejemplos:

```text
feat(web): añadir historial de verificaciones en dashboard
fix(api): corregir timeout en búsqueda GDELT
docs: actualizar guía de demo para jurado
```

## Pull Requests

- Usa la plantilla que aparece al abrir el PR.
- Enlaza el issue relacionado (`Closes #12`).
- Incluye capturas si cambias la UI.
- Comprueba localmente antes de pedir review:
  - API: `uvicorn main:app --reload --port 8000` en `api/`
  - Web: `npm run dev` en `web/`
- Responde a los comentarios de review; no merges tu propio PR sin al menos una aprobación.

## Code review

Al revisar un PR, comprueba:

- [ ] El cambio resuelve el issue / tarea acordada.
- [ ] No introduce secretos (`.env`, API keys, tokens).
- [ ] La app arranca o el build pasa (CI verde).
- [ ] Documentación actualizada si cambia comportamiento visible.

Sé constructivo: sugiere mejoras concretas, aprueba cuando esté listo.

## Issues

- **Bug:** usa la plantilla _Reporte de bug_.
- **Feature / mejora:** usa la plantilla _Solicitud de funcionalidad_.
- Asigna etiquetas y responsable si el equipo las usa (`bug`, `enhancement`, `docs`, `good first issue`).

## Estructura del repo (dónde tocar)

| Carpeta | Responsabilidad típica |
|---------|------------------------|
| `api/` | Backend FastAPI, verificadores, agregador de noticias |
| `web/` | Frontend Next.js |
| `extension/` | Extensión Chrome |
| `config/` | YAML de keywords, fuentes, catálogos |
| `docs/` | Documentación de equipo, demo y metodología |
| `tools/` | Scripts auxiliares |

Evita commits masivos que mezclen API + web + docs sin motivo; facilita el review.

## CI (GitHub Actions)

Cada PR ejecuta comprobaciones ligeras (sintaxis Python y build de Next.js). Si falla CI, corrige antes de mergear.

## Dudas

Abre un issue con la etiqueta `question` o comenta en el PR. Para decisiones de arquitectura, documenta el acuerdo en `docs/TEAM_WORKFLOW.md` o en un issue cerrado.
