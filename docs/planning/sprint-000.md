# Sprint 0 — Configuracion del Proyecto

> **Proyecto:** TaskRegistry
> **Sprint:** 0 (Setup)
> **Duracion estimada:** 1 sesion
> **Objetivo:** Tener el proyecto configurado, funcional y versionado en GitHub, listo para comenzar el desarrollo de modulos.

---

## Tareas del Sprint 0

| # | Tarea | Descripcion | Archivos creados |
|---|-------|-------------|------------------|
| 1 | Instalar pip | Solucionar la falta de pip en Python 3.13.7 | — |
| 2 | Crear entorno virtual y estructura de carpetas | Preparar el layout del proyecto | Estructura completa de directorios y `__init__.py` |
| 3 | Crear archivos de configuracion del proyecto | Dependencias,工具 config, variables de entorno | `requirements.txt`, `pyproject.toml`, `.env`, `.env.example`, `.gitignore` |
| 4 | Configurar el core del proyecto | Settings, database, dependencies, logging | `core/config.py`, `core/database.py`, `core/dependencies.py`, `core/logging_config.py` |
| 5 | Crear punto de entrada de la app | Aplicacion FastAPI funcional | `main.py`, `run.py`, `run.bat` |
| 6 | Inicializar Git y conectar con GitHub | Repo local -> remoto | — |
| 7 | Configurar VS Code | Extensiones y settings recomendados | `.vscode/extensions.json` |
| 8 | Configurar GitHub Actions (CI) | Lint + test automaticos | `.github/workflows/ci.yml`, `.github/workflows/pr-validation.yml` |
| 9 | Verificacion final | Probar que todo funciona | — |

---

## Tarea 1: Instalar pip

### Problema
Python 3.13.7 esta instalado pero pip no estaba disponible (error `ModuleNotFoundError: No module named 'pip'`).

### Que se hizo
- Descargar el script `get-pip.py` desde `https://bootstrap.pypa.io/get-pip.py`
- Ejecutar el script para instalar pip
- Verificar la instalacion con `python -m pip --version`

### Resultado
pip 26.1.2 instalado y funcionando para Python 3.13.7.

---

## Tarea 2: Crear entorno virtual y estructura de carpetas

### Que se hizo
- Crear entorno virtual con `python -m venv venv`
- Activar el entorno virtual
- Crear toda la estructura de directorios del proyecto
- Crear archivos `__init__.py` en cada paquete Python

### Estructura resultante

```
C:\Repos\Personal\IA\TaskRegistry\
│
├── core/
│   └── __init__.py
├── proyectos/
│   ├── __init__.py
│   └── templates/
│       └── proyectos/
├── tareas/
│   ├── __init__.py
│   └── templates/
│       └── tareas/
├── documentos/
│   ├── __init__.py
│   └── templates/
│       └── documentos/
├── sincronizacion/
│   ├── __init__.py
│   └── templates/
│       └── sincronizacion/
├── tablero/
│   ├── __init__.py
│   └── templates/
│       └── tablero/
├── static/
│   ├── css/
│   └── js/
├── data/
│   └── docs/
├── tests/
│   ├── __init__.py
│   ├── core/
│   ├── proyectos/
│   ├── tareas/
│   ├── sincronizacion/
│   └── tablero/
├── .github/
│   └── workflows/
├── .vscode/
└── venv/                  # (entorno virtual, no tocar)
```

---

## Tarea 3: Crear archivos de configuracion del proyecto

### Archivos creados

| Archivo | Proposito | Contenido principal |
|---------|-----------|---------------------|
| `requirements.txt` | Dependencias del proyecto | fastapi, uvicorn, sqlmodel, alembic, pydantic-settings, jinja2, httpx, ruff, pytest |
| `pyproject.toml` | Configuracion de herramientas | Ruff (line-length=100, doble comilla), pytest (testpaths = tests) |
| `.env` | Variables de entorno local (gitignorado) | APP_NAME, DATABASE_URL, Azure DevOps creds |
| `.env.example` | Plantilla para otros desarrolladores | Mismas variables que .env pero con valores vacios |
| `.gitignore` | Archivos ignorados por Git | venv/, data/, __pycache__/, .env, .vscode/settings.json |

### Resultado
Dependencias instaladas (39 paquetes). Ruff check: `All checks passed!`.

---

## Tarea 4: Configurar el core del proyecto

### Archivos creados en `core/`

| Archivo | Proposito | Lo que implementa |
|---------|-----------|-------------------|
| `config.py` | Configuracion centralizada | Clase `Settings` con pydantic-settings que lee variables de `.env` |
| `database.py` | Configuracion de base de datos | Engine SQLAlchemy para SQLite, `create_db_and_tables()`, `get_session()` |
| `dependencies.py` | Fábricas de dependencias FastAPI | `get_db()` para inyectar sesion BD, `get_logger()` |
| `logging_config.py` | Configuracion de logging | Salida a consola + archivo `data/taskregistry.log` |

### Detalles de configuracion
- **Settings**: Lee APP_NAME, APP_VERSION, DEBUG, LOG_LEVEL, DATABASE_URL, Azure DevOps variables desde `.env`
- **Database**: SQLite con `check_same_thread=False`, engine singleton
- **Dependencies**: `get_db()` como generator para FastAPI Depends
- **Logging**: Formato con timestamp, nivel, modulo, funcion y mensaje

---

## Tarea 5: Crear punto de entrada de la aplicacion

### Archivos creados en la raiz

| Archivo | Proposito |
|---------|-----------|
| `main.py` | Punto de entrada FastAPI con `create_app()` |
| `run.py` | Script de desarrollo con uvicorn (reload activo) |
| `run.bat` | Acceso directo Windows que activa venv y ejecuta run.py |

### Que implementa `main.py`
- Funcion `create_app()` que crea instancia de FastAPI
- Configura logging al arrancar
- Crea tablas de BD en el evento startup
- Monta archivos estaticos desde `static/`
- Redirige raiz a Swagger UI (`/docs`)
- Placeholder para registrar routers de modulos (comentado)

---

## Tarea 6: Inicializar Git y conectar con GitHub

### Que se hizo
1. Inicializar repositorio local con `git init`
2. Agregar todos los archivos con `git add .`
3. Commit inicial con mensaje convencional (`chore: initial project setup...`)
4. Verificar que Ruff no encuentra errores
5. Crear repositorio en GitHub (`task-registry`, privado)
6. Conectar local con remoto y hacer push a `origin/main`

### Commit message
```
chore: initial project setup (Sprint 0)

- Project structure with modular domain organization
- Core configuration (settings, database, logging)
- Dependencies (requirements.txt) and tooling config (pyproject.toml)
- VS Code workspace settings
- CI workflow for lint and test
```

---

## Tarea 7: Configurar VS Code

### Extensiones recomendadas

| Extension | ID | Proposito |
|-----------|-----|-----------|
| Python | `ms-python.python` | Soporte Python (intellisense, debugging) |
| Ruff | `charliermarsh.ruff` | Linter y formateador integrado |
| Jinja | `wholroyd.jinja` | Syntax highlighting para templates |
| HTMX | `mrmlnc.vscode-htmx` | Resalta etiquetas HTMX en HTML |
| GitLens | `eamodio.gitlens` | Visualizacion avanzada de Git |
| Todo Tree | `Gruntfuggly.todo-tree` | Resalta comentarios TODO/FIXME |

Se creo `.vscode/extensions.json` con las recomendaciones.

---

## Tarea 8: Configurar GitHub Actions (CI/CD)

### Archivos creados en `.github/workflows/`

| Archivo | Proposito | Jobs |
|---------|-----------|------|
| `ci.yml` | CI en push/PR a main | lint (ruff check + format) + test (pytest --cov) |
| `pr-validation.yml` | Validacion de PRs | Conventional commits + branch naming |

### Que valida el CI
- **lint**: Ejecuta `ruff check .` y `ruff format . --check` en Ubuntu con Python 3.13
- **test**: Ejecuta `pytest -v --cov=.` para verificar que todos los tests pasan

---

## Tarea 9: Verificacion final

### Checklist de verificacion

- [x] **pip funciona**: `python -m pip --version` muestra la version
- [x] **Entorno virtual activo**: `(venv)` visible en la terminal
- [x] **Dependencias instaladas**: import fastapi funciona correctamente
- [x] **Estructura de carpetas**: todas las carpetas existen
- [x] **Ruff no reporta errores**: `ruff check .` sale limpio
- [x] **La app arranca**: `python run.py` inicia el servidor sin errores
- [x] **Swagger UI funciona**: `http://localhost:8000/docs` accesible
- [x] **Git en GitHub**: commit inicial presente en `origin/main`

---

## Resumen de archivos creados en Sprint 0

| Archivo | Proposito |
|---------|-----------|
| `main.py` | Punto de entrada FastAPI |
| `run.py` | Script de desarrollo con uvicorn |
| `run.bat` | Acceso directo Windows |
| `requirements.txt` | Dependencias del proyecto |
| `pyproject.toml` | Configuracion de herramientas (Ruff, pytest) |
| `.env` | Variables de entorno local (gitignorado) |
| `.env.example` | Plantilla de variables de entorno |
| `.gitignore` | Archivos ignorados por Git |
| `core/__init__.py` | Paquete core |
| `core/config.py` | Configuracion con pydantic-settings |
| `core/database.py` | Engine y sesion de base de datos |
| `core/dependencies.py` | Fábricas de dependencias FastAPI |
| `core/logging_config.py` | Configuracion de logging |
| `proyectos/__init__.py` | Paquete proyectos (vacio, listo para implementar) |
| `tareas/__init__.py` | Paquete tareas (vacio) |
| `documentos/__init__.py` | Paquete documentos (vacio) |
| `sincronizacion/__init__.py` | Paquete sincronizacion (vacio) |
| `tablero/__init__.py` | Paquete tablero (vacio) |
| `tests/__init__.py` (y subpaquetes) | Paquete de tests |
| `tests/test_config.py` | Tests de configuracion |
| `tests/test_database.py` | Tests de base de datos |
| `tests/test_dependencies.py` | Tests de dependencias |
| `tests/test_logging_config.py` | Tests de logging |
| `tests/test_main.py` | Tests del punto de entrada |
| `.github/workflows/ci.yml` | CI con Ruff + pytest |
| `.github/workflows/pr-validation.yml` | Validacion de PRs |
| `.vscode/extensions.json` | Extensiones recomendadas |

---

## Criterios de aceptacion del Sprint 0

- [x] La aplicacion arranca sin errores con `python run.py`
- [x] Swagger UI es accesible en `http://localhost:8000/docs`
- [x] Ruff no reporta errores con `ruff check .`
- [x] El repositorio esta en GitHub con el commit inicial
- [x] El README.md tiene instrucciones de instalacion
- [x] Todos los modulos tienen su estructura de carpetas creada (aunque vacia)
