# ADR-001: Stack Tecnológico

- **Estado:** Aceptado
- **Fecha:** 2026-06-20
- **Contexto:** Sesión de definición arquitectónica con el desarrollador

---

## Decisión

| Componente | Elección |
|------------|----------|
| Tipo de aplicación | Web local (servidor Python + navegador) |
| Framework backend | FastAPI |
| Frontend | Jinja2 + HTMX + Alpine.js |
| Base de datos | SQLite |
| ORM | SQLModel |
| Linter / Formatter | Ruff |

---

## Opciones Consideradas

### Framework Backend
- **FastAPI** ✅ — Async nativo, validación con Pydantic, Swagger UI integrado, ideal para CRUD + API externa
- **Flask** — Válido pero requiere más extensiones para features que FastAPI trae nativas
- **Django** — Sobredimensionado para app single-user sin autenticación

### Frontend
- **Jinja2 + HTMX + Alpine.js** ✅ — Sin build step, interactividad SPA-like, un solo lenguaje (Python + HTML)
- **React/Vue/Svelte** — Más potencia pero introduce Node.js, build step y complejidad innecesaria para este alcance
- **Jinja2 puro** — Válido pero menos interactivo para filtros en vivo del tablero

### ORM
- **SQLModel** ✅ — Unifica modelos BD con esquemas Pydantic, del autor de FastAPI, mínimo boilerplate
- **SQLAlchemy** — Más maduro pero más verboso; SQLModel es suficiente para el alcance del proyecto
- **SQL puro** — Sin dependencias pero mucho código repetitivo y propenso a errores

### Linter / Formatter
- **Ruff** ✅ — Todo-en-uno (linter + formatter), escrito en Rust, extremadamente rápido
- **Pylint + Black** — Clásico pero más lento y requiere dos herramientas

---

## Consecuencias

- Stack 100% Python (excepto HTMX/Alpine.js que son CDN)
- Sin build step en frontend — el HTML se sirve directamente
- Swagger UI en `/docs` disponible para debugging de integración Azure
- Migraciones de BD con Alembic (vía SQLModel)
