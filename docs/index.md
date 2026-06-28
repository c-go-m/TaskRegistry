# TaskRegistry — Índice de Documentación

> **Bitácora personal de tareas laborales con sincronización a Azure DevOps**

---

## 🚀 Para nuevos desarrolladores / Agentes

| Si necesitas... | Ve a... |
|----------------|---------|
| Entender el proyecto, su propósito y stack | [`docs/general/README.md`](./general/README.md) |
| Poner el proyecto en marcha (rápido) | [`README.md`](../README.md#-cómo-empezar) |
| Ver la estructura de carpetas | [`docs/architecture/estructura-propuesta.md`](./architecture/estructura-propuesta.md) |
| Conocer las reglas de negocio del sistema | [`docs/general/06-Reglas-Negocio.md`](./general/06-Reglas-Negocio.md) |
| Entender las decisiones técnicas (ADRs) | [`docs/architecture/README.md`](./architecture/README.md) |

---

## 📦 Documentación por módulo

| # | Módulo | Descripción | Documento |
|---|--------|-------------|-----------|
| 1 | **Proyectos** | CRUD de proyectos: creación, edición, archivado | [`01-Modulo-Proyectos.md`](./general/01-Modulo-Proyectos.md) |
| 2 | **Tareas** | Registro diario de tareas con fechas, tiempos y estados | [`02-Modulo-Tareas.md`](./general/02-Modulo-Tareas.md) |
| 3 | **Documentación** | Documentos y archivos adjuntos asociados a proyectos | [`03-Modulo-Documentacion.md`](./general/03-Modulo-Documentacion.md) |
| 4 | **Sincronización Azure** | Sincronización batch de tareas a Azure DevOps | [`04-Modulo-Sincronizacion-Azure.md`](./general/04-Modulo-Sincronizacion-Azure.md) |
| 5 | **Tablero de Control** | Métricas y visualización de tareas y tiempos | [`05-Modulo-Tablero-Control.md`](./general/05-Modulo-Tablero-Control.md) |
| — | **Reglas de Negocio** | Reglas generales que aplican a todo el sistema | [`06-Reglas-Negocio.md`](./general/06-Reglas-Negocio.md) |

---

## 🏗️ Arquitectura

| Documento | Descripción |
|-----------|-------------|
| [Diagrama de Contexto (C4 N1)](./architecture/diagrama-contexto.md) | Actores y sistemas externos |
| [Diagrama de Contenedores (C4 N2)](./architecture/diagrama-contenedores.md) | Componentes internos y sus interacciones |
| [Estructura del proyecto](./architecture/estructura-propuesta.md) | Árbol de directorios completo |
| [ADR-001: Stack tecnológico](./architecture/ADR-001-stack-tecnologico.md) | FastAPI, Jinja2+HTMX+Alpine.js, SQLite, SQLModel, Ruff |
| [ADR-002: Estructura del proyecto](./architecture/ADR-002-estructura-proyecto.md) | Organización modular por dominio |
| [ADR-003: Patrones de diseño](./architecture/ADR-003-patrones-diseno.md) | Router → Service → Repository → Model + DI |
| [ADR-004: DevOps / CI-CD](./architecture/ADR-004-devops.md) | GitHub, GitHub Actions, Conventional Commits |

---

## 📋 Planificación

| Documento | Descripción |
|-----------|-------------|
| [Backlog completo](./planning/backlog.md) | Épicas e historias de usuario |
| [Sprint 0 (completado)](./planning/sprint-000.md) | Configuración inicial del proyecto |
| [Definition of Done](./planning/definition-of-done.md) | Criterios de aceptación para tareas |

---

## 💻 Comandos rápidos

### Iniciar el proyecto

```powershell
.\venv\Scripts\activate   # Activar entorno virtual
python run.py             # Iniciar servidor (http://localhost:8000)
```

### Linter y formateo

```powershell
ruff check .              # Verificar lint
ruff format . --check     # Verificar formato (sin modificar)
ruff format .             # Formatear archivos automáticamente
```

### Tests

```powershell
pytest -v                 # Ejecutar tests (verbose)
pytest --cov=.            # Ejecutar tests con cobertura
```

### Commits

```powershell
git commit -m "tipo(alcance): descripción"
# Tipos: feat, fix, chore, docs, style, refactor, perf, test, build, ci, revert
```
