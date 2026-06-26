# Flujo de trabajo en equipo — The NewsBreakers

Guía práctica para colaborar en el repositorio [The-NewsBreakers](https://github.com/JAVGP444/The-NewsBreakers) durante el datathon, el portfolio académico y la preparación de la demo ante jurado.

## Resumen ejecutivo

| Decisión | Recomendación |
|----------|---------------|
| Plataforma principal | **GitHub** (issues, PRs, Actions) |
| Rama estable | `master` (actual) o renombrar a `main` |
| Rama de integración | `develop` (crear una vez y usarla como base) |
| Ramas de trabajo | `feature/*`, `fix/*` |
| Edición simultánea | GitHub Codespaces o VS Code Live Share como complemento |
| Protección | Activar branch protection en `master` (y opcionalmente `develop`) |

Documentos relacionados:

- [.github/CONTRIBUTING.md](../.github/CONTRIBUTING.md) — reglas de contribución
- [README.md](../README.md) — inicio rápido técnico
- [docs/DEMO.md](./DEMO.md) — guía de presentación

---

## 1. Estado actual del repositorio

Al configurar este flujo, el repo tenía:

- **Remoto:** `https://github.com/JAVGP444/The-NewsBreakers.git`
- **Rama principal:** `master` (sin rama `develop` todavía)
- **Estructura principal:**

```text
the-newsbreakers/
├── api/          # Backend FastAPI
├── web/          # Frontend Next.js
├── extension/    # Extensión Chrome
├── config/       # YAML (keywords, fuentes, catálogos)
├── docs/         # Documentación
├── tools/        # Scripts auxiliares
├── scripts/      # Arranque en Windows (PowerShell)
└── assets/       # PDFs, imágenes, excels
```

### Nota sobre rutas en Windows

En Windows el explorador de archivos muestra `api\main.py`, pero **Git siempre usa barras normales** (`api/main.py`). No existen carpetas duplicadas `api\` y `api/`; es la misma ruta con distinto separador. Lo mismo aplica a `docs/`.

### Trabajo local sin commitear

Si hay muchos archivos nuevos o modificados solo en tu máquina (por ejemplo módulos en `api/` aún no subidos), **sincroniza con el equipo antes de invitar colaboradores**: decidid quién integra qué, abrid un PR grande inicial o repartid por features para evitar conflictos masivos.

---

## 2. Modelo de ramas recomendado

```mermaid
gitGraph
   commit id: "master estable"
   branch develop
   checkout develop
   commit id: "integración"
   branch feature/ejemplo
   checkout feature/ejemplo
   commit id: "trabajo"
   checkout develop
   merge feature/ejemplo
   checkout master
   merge develop tag: "release demo"
```

| Rama | Quién mergea | Cuándo |
|------|--------------|--------|
| `feature/*` | Autor vía PR → `develop` | Cada tarea / issue |
| `develop` | Maintainer tras review | Integración continua |
| `master` | Maintainer tras demo estable | Entregas, hitos, versión para jurado |

### Crear `develop` (una sola vez)

Desde tu máquina, con el repo actualizado:

```powershell
git checkout master
git pull origin master
git checkout -b develop
git push -u origin develop
```

En GitHub → **Settings → Branches**, puedes marcar `develop` como rama por defecto para PRs diarios y reservar `master` para releases.

### Convención de nombres

```text
feature/dashboard-historial
feature/fuentes-woah
fix/timeout-gdelt
docs/guia-jurado
```

---

## 3. Flujo diario (GitHub)

1. **Tomar tarea:** crear o asignarse un [issue](https://github.com/JAVGP444/The-NewsBreakers/issues).
2. **Actualizar base:**
   ```powershell
   git checkout develop
   git pull origin develop
   git checkout -b feature/mi-tarea
   ```
3. **Desarrollar y commitear** en commits pequeños.
4. **Push y Pull Request** hacia `develop` (usa la plantilla automática).
5. **Code review:** al menos un compañero aprueba (ver CODEOWNERS).
6. **Merge** cuando CI esté en verde.
7. **Release / demo:** PR de `develop` → `master` cuando el equipo acuerde que está listo.

Detalle de commits y review: [.github/CONTRIBUTING.md](../.github/CONTRIBUTING.md).

---

## 4. Alternativas para programar en equipo

### A) GitHub (recomendado — fuente de verdad)

- Historial, issues, PRs y CI en un solo sitio.
- Ideal para portfolio: el jurado puede ver commits, PRs y documentación.
- **Usad siempre GitHub como referencia final**, aunque editéis en pareja con otras herramientas.

### B) GitHub Codespaces

Entorno en la nube con VS Code en el navegador, útil si no todos tienen Python/Node bien configurados.

1. Repo → **Code** → pestaña **Codespaces** → **Create codespace on develop**.
2. Terminal integrada:
   ```bash
   cd api && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
   ```
   En otra terminal:
   ```bash
   cd web && npm install && npm run dev
   ```
3. Codespaces reenvía puertos automáticamente (8000 API, 3003 web).

**Ventajas:** mismo entorno para todos, cero “en mi máquina funciona”.  
**Contras:** minutos gratuitos limitados; requiere cuenta GitHub.

### C) VS Code Live Share

Sesión compartida en tiempo real (un host, varios invitados). Bueno para pair programming en la misma feature.

- Instalar extensión **Live Share** en VS Code / Cursor.
- Host: **Share** → invitados editan juntos.
- **Importante:** al terminar la sesión, el código debe quedar en una rama y subirse con PR; Live Share no sustituye a Git.

### D) Branch protection en `master`

En GitHub → **Settings → Branches → Add branch protection rule**:

- Branch name pattern: `master` (y opcionalmente `develop`)
- ☑ Require a pull request before merging
- ☑ Require approvals (1)
- ☑ Require status checks to pass (seleccionar jobs de CI: `API — sintaxis Python`, `Web — build Next.js`)
- ☑ Do not allow bypassing (opcional, según confianza del equipo)

Así nadie pushea directamente a producción/demo por accidente.

---

## 5. Desarrollo local vs Codespaces

### Local (Windows — scripts incluidos)

```powershell
# Terminal 1 — API
cd api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Web
cd web
npm install
npm run dev
```

Scripts de conveniencia en `scripts/` (`iniciar.ps1`, `iniciar-background.ps1`, etc.).

Variables de entorno:

| Archivo | Uso |
|---------|-----|
| `api/.env.example` | Copiar a `api/.env` (no commitear) |
| `web/.env.example` | Copiar a `web/.env.local` si necesitas otra URL de API |

### Checklist antes de abrir un PR

- [ ] API arranca sin errores en `/docs`
- [ ] Web carga en `http://localhost:3003`
- [ ] No hay `.env` ni claves en el diff
- [ ] CI local opcional: `npm run build` en `web/`

---

## 6. CI automático (GitHub Actions)

El workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) ejecuta en cada PR y push a `master` / `develop`:

1. **API:** instala dependencias, `compileall` e imports básicos.
2. **Web:** `npm ci` + `npm run build`.

No requiere secretos. Si falla, corregid antes de mergear.

---

## 7. Roles sugeridos (equipo pequeño)

| Rol | Responsabilidad |
|-----|-----------------|
| **Maintainer** (@JAVGP444 inicialmente) | Merge a `master`, protección de ramas, invites |
| **Backend** | `api/`, `config/`, integraciones GDELT/fuentes |
| **Frontend** | `web/`, UX demo, dashboard |
| **Docs / demo** | `docs/`, `assets/pdfs`, guión jurado |

Actualiza [.github/CODEOWNERS](../.github/CODEOWNERS) cuando añadas compañeros:

```text
/api/ @JAVGP444 @usuario-backend
/web/ @JAVGP444 @usuario-frontend
```

---

## 8. Tips para portfolio y presentación

1. **README claro** — ya describe arquitectura y quick start; mantenedlo al día.
2. **PRs visibles** — muestran trabajo en equipo y revisión por pares (valorado en datathons).
3. **Issues con criterios de aceptación** — demuestra planificación ágil ligera.
4. **Demo reproducible** — jurado puede clonar y ejecutar en 5 minutos (ver [DEMO.md](./DEMO.md)).
5. **Arquitectura en un diagrama** — [ARQUITECTURA-TECNICA.md](./ARQUITECTURA-TECNICA.md) para profundidad técnica.
6. **Tag de release** en `master` antes de la entrega:
   ```powershell
   git checkout master
   git pull
   git tag -a v1.0-demo -m "Versión presentación datathon"
   git push origin v1.0-demo
   ```

---

## 9. Próximos pasos para el maintainer

Checklist para activar el flujo en GitHub:

1. [ ] Revisar y commitear el trabajo local pendiente (o repartirlo en PRs).
2. [ ] Subir estos archivos de `.github/` y `docs/TEAM_WORKFLOW.md`.
3. [ ] Crear rama `develop` y push (`git push -u origin develop`).
4. [ ] **Settings → Collaborators** → invitar al equipo por usuario GitHub.
5. [ ] Activar **branch protection** en `master` (sección 4D).
6. [ ] (Opcional) Cambiar default branch a `develop` para PRs diarios.
7. [ ] Actualizar **CODEOWNERS** con usuarios reales del equipo.
8. [ ] Crear issues iniciales por área (API, web, docs demo).
9. [ ] Probar un PR de prueba para verificar CI y plantillas.

---

## 10. Recursos

- [GitHub Flow (oficial)](https://docs.github.com/en/get-started/using-github/github-flow)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Codespaces](https://docs.github.com/en/codespaces)
- [VS Code Live Share](https://visualstudio.microsoft.com/services/live-share/)
