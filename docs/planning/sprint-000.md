# Sprint 0 — Configuración del Proyecto

> **Proyecto:** TaskRegistry
> **Sprint:** 0 (Setup)
> **Duración estimada:** 1 sesión
> **Objetivo:** Tener el proyecto configurado, funcional y versionado en GitHub, listo para comenzar el desarrollo de módulos.

---

## 📋 Tareas del Sprint 0

| # | Tarea | Descripción | Archivos a crear/modificar |
|---|-------|-------------|---------------------------|
| 1 | ✅ Instalar pip | Solucionar la falta de pip en Python 3.13.7 | — |
| 2 | ✅ Crear entorno virtual y estructura de carpetas | Preparar el layout del proyecto | (ver estructura arriba) |
| 3 | ✅ Crear archivos de configuración del proyecto | `requirements.txt`, `pyproject.toml`, `.env`, `.env.example`, `.gitignore` | Múltiples |
| 4 | ✅ Configurar el core del proyecto | `config.py`, `database.py`, `dependencies.py`, `logging_config.py` | `core/` |
|   | ✅ Completada el 2026-06-28 | | |
| 5 | ✅ Crear punto de entrada de la app | `main.py` + `run.py` + `run.bat` | Raíz del proyecto |
|   | ✅ Completada el 2026-06-28 | | |
| 6 | ✅ Inicializar Git y conectar con GitHub | Repo local → GitHub remoto | — |
|   | ✅ Completada el 2026-06-28 | | |
| 7 | ✅ Configurar VS Code | Extensiones y settings recomendados | `.vscode/` |
|   | ✅ Completada el 2026-06-28 | | |
| 8 | ✅ Configurar GitHub Actions (CI) | Lint + test automáticos | `.github/workflows/` |
|   | ✅ Completada el 2026-06-28 | | |
| 9 | ✅ Verificación final | Probar que todo funciona | — |
|   | ✅ Completada el 2026-06-28 | | |

---

## 🧩 Tarea 1: Instalar pip

### Problema
Python 3.13.7 está instalado pero **pip no está disponible** (da error `ModuleNotFoundError: No module named 'pip'`).

### Solución paso a paso

1. Abre una terminal **como administrador** (Windows: botón derecho en "Símbolo del sistema" o "PowerShell" → "Ejecutar como administrador")

2. Descarga el script de instalación de pip:
   ```powershell
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   ```

3. Ejecuta el script para instalar pip:
   ```powershell
   python get-pip.py
   ```

4. Verifica que pip se instaló correctamente:
   ```powershell
   python -m pip --version
   ```
   Deberías ver algo como: `pip 25.x from C:\Users\gomezcam\...\site-packages\pip (python 3.13)`

5. (Opcional) Elimina el archivo `get-pip.py`:
   ```powershell
   del get-pip.py
   ```

> ✅ **Completada el 2026-06-28** — pip 26.1.2 instalado y funcionando para Python 3.13.7.

---

## 🧩 Tarea 2: Crear entorno virtual y estructura de carpetas

### 2.1 Crear el entorno virtual

En la raíz del proyecto (`C:\Repos\Personal\IA\TaskRegistry\`), ejecuta:

```powershell
python -m venv venv
```

Esto crea una carpeta `venv/` con un Python aislado para el proyecto.

### 2.2 Activar el entorno virtual

```powershell
.\venv\Scripts\activate
```

Deberías ver `(venv)` al inicio de la línea en la terminal.

### 2.3 Crear la estructura de carpetas

Ejecuta este comando en PowerShell desde la raíz del proyecto:

```powershell
# Crear estructura de directorios
New-Item -ItemType Directory -Path "core" -Force
New-Item -ItemType Directory -Path "proyectos", "proyectos\templates\proyectos" -Force
New-Item -ItemType Directory -Path "tareas", "tareas\templates\tareas" -Force
New-Item -ItemType Directory -Path "documentos", "documentos\templates\documentos" -Force
New-Item -ItemType Directory -Path "sincronizacion", "sincronizacion\templates\sincronizacion" -Force
New-Item -ItemType Directory -Path "tablero", "tablero\templates\tablero" -Force
New-Item -ItemType Directory -Path "static\css", "static\js" -Force
New-Item -ItemType Directory -Path "data\docs" -Force
New-Item -ItemType Directory -Path "tests\proyectos", "tests\tareas", "tests\sincronizacion", "tests\tablero" -Force
New-Item -ItemType Directory -Path ".github\workflows" -Force
New-Item -ItemType Directory -Path ".vscode" -Force
```

### 2.4 Crear archivos `__init__.py` vacíos

Python necesita estos archivos para reconocer las carpetas como paquetes:

```powershell
# Crear __init__.py en cada paquete
@"" | Out-File -FilePath "core\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "proyectos\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tareas\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "documentos\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "sincronizacion\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tablero\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tests\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tests\proyectos\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tests\tareas\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tests\sincronizacion\__init__.py" -Encoding utf8
@"" | Out-File -FilePath "tests\tablero\__init__.py" -Encoding utf8
```

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

## 🧩 Tarea 3: Crear archivos de configuración del proyecto

### 3.1 `requirements.txt`

Crea el archivo `requirements.txt` en la raíz con este contenido:

```txt
# Framework
fastapi==0.115.0
uvicorn[standard]==0.30.0

# Base de datos
sqlmodel==0.0.22
alembic==1.13.0

# Configuración
pydantic-settings==2.5.0
python-dotenv==1.0.1

# Templates
jinja2==3.1.4
aiofiles==24.1.0
python-multipart==0.0.12

# Cliente HTTP (para Azure DevOps API)
httpx==0.27.0

# Desarrollo
ruff==0.6.0
pytest==8.3.0
pytest-cov==5.0.0
httpx==0.27.0               # también usado en tests para TestClient
```

### 3.2 Instalar dependencias

Con el entorno virtual activo (`(venv)` visible):

```powershell
python -m pip install -r requirements.txt
```

### 3.3 `pyproject.toml`

Configura Ruff y pytest. Crea este archivo en la raíz:

```toml
[project]
name = "task-registry"
version = "0.1.0"
description = "Bitácora personal de tareas laborales con sincronización a Azure DevOps"
requires-python = ">=3.12"

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.ruff.format]
quote-style = "double"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

### 3.4 `.env` (local, gitignorado)

```env
# Configuración de la aplicación
APP_NAME=TaskRegistry
APP_VERSION=0.1.0
DEBUG=true
LOG_LEVEL=DEBUG

# Base de datos
DATABASE_URL=sqlite:///data/taskregistry.db

# Azure DevOps (opcional, se configura después)
AZURE_DEVOPS_ORG=
AZURE_DEVOPS_PROJECT=
AZURE_DEVOPS_PAT=
```

### 3.5 `.env.example` (plantilla para otros desarrolladores)

Copia el mismo contenido que `.env` pero con valores vacíos o de ejemplo. Es el archivo que se versiona en Git.

### 3.6 `.gitignore`

```gitignore
# Entorno virtual
venv/
.venv/

# Datos de usuario
data/
!data/.gitkeep

# Archivos de entorno local
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/

# VS Code (settings personales)
.vscode/settings.json
.vscode/launch.json

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
*.swp
*.swo

# Logs
*.log
```

> ✅ **Completada el 2026-06-28** — Archivos `requirements.txt`, `pyproject.toml`, `.env`, `.env.example` y `.gitignore` creados. Dependencias instaladas (39 paquetes). Ruff check: `All checks passed!`.

---

## 🧩 Tarea 4: Configurar el core del proyecto

### 4.1 `core/config.py`

Configuración centralizada usando `pydantic-settings`:

```python
"""Configuración de la aplicación usando pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Metadatos
    app_name: str = "TaskRegistry"
    app_version: str = "0.1.0"
    debug: bool = True
    log_level: str = "DEBUG"

    # Base de datos
    database_url: str = "sqlite:///data/taskregistry.db"

    # Azure DevOps
    azure_devops_org: str = ""
    azure_devops_project: str = ""
    azure_devops_pat: str = ""

    # Rutas
    data_dir: Path = Path("data")
    docs_dir: Path = Path("data/docs")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
```

### 4.2 `core/database.py`

Configuración de SQLAlchemy/SQLModel:

```python
"""Configuración de la base de datos."""

from pathlib import Path

from sqlmodel import SQLModel, create_engine
from sqlmodel import Session as DBSession

from core.config import settings


def get_engine():
    """Crea y retorna el engine de SQLAlchemy."""
    db_path = Path(settings.database_url.replace("sqlite:///", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},  # SQLite específico
    )
    return engine


engine = get_engine()


def create_db_and_tables():
    """Crea todas las tablas definidas en los modelos SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Generador de sesiones de base de datos (para dependencias FastAPI)."""
    with DBSession(engine) as session:
        yield session
```

### 4.3 `core/dependencies.py`

Fábricas de dependencias para FastAPI:

```python
"""Fábricas de dependencias para FastAPI."""

import logging
from collections.abc import Generator

from fastapi import Depends
from sqlmodel import Session

from core.database import get_session

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """Dependencia que provee una sesión de base de datos."""
    yield from get_session()


def get_logger() -> logging.Logger:
    """Dependencia que provee un logger configurado."""
    return logger
```

### 4.4 `core/logging_config.py`

```python
"""Configuración de logging centralizada."""

import logging
import sys
from pathlib import Path

from core.config import settings


def setup_logging():
    """Configura el logging para la aplicación."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar logging a consola
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.DEBUG),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Opcional: logging a archivo
    log_dir = Path("data")
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(
        log_dir / "taskregistry.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logging.getLogger().addHandler(file_handler)

    logging.info("Logging configurado correctamente")
```

---

## 🧩 Tarea 5: Crear punto de entrada de la aplicación

### 5.1 `main.py`

```python
"""Punto de entrada de la aplicación TaskRegistry."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.database import create_db_and_tables
from core.logging_config import setup_logging

# Lista de routers que se irán agregando con cada módulo
# from proyectos.router import router as proyectos_router


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI."""
    # Configurar logging
    setup_logging()

    # Crear la aplicación
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Bitácora personal de tareas laborales",
    )

    # Crear tablas de base de datos (si no existen)
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Montar archivos estáticos
    static_dir = Path("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")

    # Registrar routers (se irán agregando)
    # app.include_router(proyectos_router, prefix="/proyectos", tags=["Proyectos"])

    # Redirigir raíz a Swagger UI (temporal, luego será al dashboard)
    @app.get("/")
    def root():
        return RedirectResponse(url="/docs")

    return app


app = create_app()
```

### 5.2 `run.py`

```python
"""Script para ejecutar la aplicación en desarrollo."""

import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
    )
```

### 5.3 `run.bat` (acceso directo Windows)

```bat
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python run.py
pause
```

---

## 🧩 Tarea 6: Inicializar Git y conectar con GitHub

### 6.1 Inicializar repositorio local

```powershell
git init
git add .
git commit -m "chore: initial project setup (Sprint 0)

- Project structure with modular domain organization
- Core configuration (settings, database, logging)
- Dependencies (requirements.txt) and tooling config (pyproject.toml)
- VS Code workspace settings
- CI workflow for lint and test"
```

### 6.2 Verificar que `ruff` no encuentra errores

```powershell
ruff check .
ruff format . --check
```

Si hay errores, corrígelos antes del commit.

### 6.3 Crear el repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `task-registry`
3. Descripción: "Bitácora personal de tareas laborales con sincronización a Azure DevOps"
4. Visibilidad: **Private** (recomendado para datos personales) o **Public**
5. **NO** marcar "Initialize this repository with a README" (ya tenemos el proyecto local)
6. Click en "Create repository"

### 6.4 Conectar local con remoto

GitHub te mostrará instrucciones. Ejecuta:

```powershell
git remote add origin https://github.com/gomezcam/task-registry.git
git branch -M main
git push -u origin main
```

> **Nota:** Si nunca has configurado Git con GitHub, puede pedirte autenticación. Te recomiendo usar **GitHub CLI** o un **Personal Access Token (PAT)**. Si necesitas ayuda con eso, avísame.

---

## 🧩 Tarea 7: Configurar VS Code

### 7.1 Extensiones recomendadas

Abre VS Code desde la terminal (estando en la raíz del proyecto):

```powershell
code .
```

Instala estas extensiones (puedes buscarlas en el marketplace o usar los siguientes comandos en la terminal integrada de VS Code):

| Extensión | ID | Por qué |
|-----------|-----|---------|
| **Python** | `ms-python.python` | Soporte Python (intellisense, debugging) |
| **Ruff** | `charliermarsh.ruff` | Linter y formateador integrado |
| **Jinja** | `wholroyd.jinja` | Syntax highlighting para templates |
| **HTMX** | `mrmlnc.vscode-htmx` | Resalta etiquetas HTMX en HTML |
| **GitLens** | `eamodio.gitlens` | Visualización avanzada de Git |
| **Todo Tree** | `Gruntfuggly.todo-tree` | Resalta comentarios TODO/FIXME |

### 7.2 `.vscode/extensions.json` (recomendaciones)

```json
{
    "recommendations": [
        "ms-python.python",
        "charliermarsh.ruff",
        "wholroyd.jinja",
        "mrmlnc.vscode-htmx",
        "eamodio.gitlens",
        "Gruntfuggly.todo-tree"
    ]
}
```

---

## 🧩 Tarea 8: Configurar GitHub Actions (CI/CD)

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Ruff lint
        run: ruff check .
      - name: Ruff format check
        run: ruff format . --check

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -v --cov=.
```

---

## 🧩 Tarea 9: Verificación final

Antes de dar por terminado el Sprint 0, verifica:

### ✅ Checklist de verificación

- [ ] **pip funciona**: `python -m pip --version` muestra la versión
- [ ] **Entorno virtual activo**: ves `(venv)` en la terminal
- [ ] **Dependencias instaladas**: `python -c "import fastapi; print('OK')"` imprime "OK"
- [ ] **Estructura de carpetas**: todas las carpetas existen (las listadas arriba)
- [ ] **Ruff no reporta errores**: `ruff check .` sale limpio
- [ ] **La app arranca**: `python run.py` inicia el servidor sin errores
- [ ] **Swagger UI funciona**: abrir `http://localhost:8000/docs` en el navegador
- [ ] **Git en GitHub**: `git log --oneline` muestra el commit inicial en `origin/main`

### Cómo probar la aplicación

1. Activa el entorno virtual: `.\venv\Scripts\activate`
2. Ejecuta: `python run.py`
3. Abre el navegador en: `http://localhost:8000/docs`
4. Deberías ver la interfaz de Swagger UI (aunque aún sin endpoints, la app está viva)

---

## 📐 Resumen de archivos creados en Sprint 0

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Punto de entrada FastAPI |
| `run.py` | Script de desarrollo con uvicorn |
| `run.bat` | Acceso directo Windows |
| `requirements.txt` | Dependencias del proyecto |
| `pyproject.toml` | Configuración de herramientas (Ruff, pytest) |
| `.env` | Variables de entorno local (gitignorado) |
| `.env.example` | Plantilla de variables de entorno |
| `.gitignore` | Archivos ignorados por Git |
| `core/__init__.py` | Paquete core |
| `core/config.py` | Configuración con pydantic-settings |
| `core/database.py` | Engine y sesión de base de datos |
| `core/dependencies.py` | Fábricas de dependencias FastAPI |
| `core/logging_config.py` | Configuración de logging |
| `proyectos/__init__.py` | Paquete proyectos (vacío, listo para implementar) |
| `tareas/__init__.py` | Paquete tareas (vacío) |
| `documentos/__init__.py` | Paquete documentos (vacío) |
| `sincronizacion/__init__.py` | Paquete sincronización (vacío) |
| `tablero/__init__.py` | Paquete tablero (vacío) |
| `tests/__init__.py` (y subpaquetes) | Paquete de tests |
| `tests/test_config.py` | Tests de configuración |
| `tests/test_database.py` | Tests de base de datos |
| `tests/test_dependencies.py` | Tests de dependencias |
| `tests/test_logging_config.py` | Tests de logging |
| `tests/test_main.py` | Tests del punto de entrada |
| `.github/workflows/ci.yml` | CI con Ruff + pytest |
| `.github/workflows/pr-validation.yml` | Validación de PRs (conventional commits, branch naming) |
| `.vscode/extensions.json` | Extensiones recomendadas |

---

## 🎯 Criterios de aceptación del Sprint 0

- [x] La aplicación arranca sin errores con `python run.py`
- [x] Swagger UI es accesible en `http://localhost:8000/docs`
- [x] Ruff no reporta errores con `ruff check .`
- [x] El repositorio está en GitHub con el commit inicial
- [x] El README.md tiene instrucciones de instalación
- [x] Todos los módulos tienen su estructura de carpetas creada (aunque vacía)
