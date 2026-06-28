# Estructura Propuesta del Proyecto

```
taskregistry/
│
├── main.py                          # Punto de entrada: crea y configura la app FastAPI
├── run.py                           # Script de desarrollo: uvicorn + logging
├── run.bat                          # Acceso directo para Windows (doble clic)
│
├── pyproject.toml                   # Configuración del proyecto (Ruff, pytest, etc.)
├── requirements.txt                 # Dependencias (pip freeze)
├── .env                             # Variables de entorno (local, gitignorado)
├── .env.example                     # Plantilla de .env para nuevos desarrolladores
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml                   # CI: lint + test + SonarCloud
│       └── release.yml              # Release: generar tag → GitHub Release
│
├── core/                            # Configuración compartida de la aplicación
│   ├── __init__.py
│   ├── config.py                    # Settings con pydantic-settings
│   ├── database.py                  # Engine, sesión, creación de tablas
│   ├── dependencies.py              # Fábricas de dependencias (get_db, get_repo, get_logger)
│   └── logging_config.py            # Configuración de logging (archivo + consola)
│
├── proyectos/                       # Módulo: Gestión de Proyectos
│   ├── __init__.py
│   ├── models.py                    # SQLModel: Proyecto
│   ├── schemas.py                   # Schemas Pydantic (request/response)
│   ├── repository.py                # ProyectoRepository (abstracto + SQLAlchemy impl)
│   ├── service.py                   # ProyectoService (reglas de negocio)
│   ├── router.py                    # Endpoints FastAPI
│   └── templates/
│       └── proyectos/
│           ├── list.html            # Lista de proyectos
│           ├── detail.html          # Detalle de proyecto (con pestañas)
│           └── form.html            # Crear/editar proyecto
│
├── tareas/                          # Módulo: Registro de Tareas
│   ├── __init__.py
│   ├── models.py                    # SQLModel: Tarea
│   ├── schemas.py
│   ├── repository.py                # TareaRepository
│   ├── service.py                   # TareaService (cálculo tiempo, transiciones estado)
│   ├── router.py
│   └── templates/
│       └── tareas/
│           ├── list.html            # Lista con filtros por proyecto/estado/fechas
│           ├── detail.html          # Detalle/edición de tarea
│           └── form.html            # Crear tarea
│
├── documentos/                      # Módulo: Documentación de Proyectos
│   ├── __init__.py
│   ├── models.py                    # SQLModel: Documento, ArchivoAdjunto
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py                   # Gestión de archivos en disco
│   ├── router.py
│   └── templates/
│       └── documentos/
│           ├── list.html
│           └── detail.html
│
├── sincronizacion/                  # Módulo: Sincronización Azure DevOps
│   ├── __init__.py
│   ├── schemas.py                   # Schemas de configuración y sincronización
│   ├── repository.py                # Acceso a configuración y tareas pendientes
│   ├── service.py                   # Lógica de sincronización (llamadas REST API)
│   ├── router.py                    # Endpoints para sincronizar
│   ├── cliente_azure.py             # Cliente HTTP para Azure DevOps REST API
│   └── templates/
│       └── sincronizacion/
│           ├── config.html          # Configuración de conexión (URL, proyecto, PAT)
│           └── sync.html            # Vista de sincronización (seleccionar tareas, HU)
│
├── tablero/                         # Módulo: Tablero de Control
│   ├── __init__.py
│   ├── schemas.py
│   ├── repository.py                # Queries de métricas (agregaciones)
│   ├── service.py                   # Cálculo de métricas
│   ├── router.py
│   └── templates/
│       └── tablero/
│           └── dashboard.html       # Tablero con filtros y métricas
│
├── static/                          # Assets estáticos globales
│   ├── css/
│   │   └── app.css                  # Estilos globales (usando Tailwind CSS vía CDN o simple CSS)
│   └── js/
│       └── app.js                   # JavaScript global (Alpine.js se carga vía CDN)
│
├── data/                            # Datos de usuario (gitignorado)
│   ├── taskregistry.db              # Base de datos SQLite
│   └── docs/                        # Archivos adjuntos de documentos
│       └── {proyecto_id}/
│           └── {documento_id}/
│               ├── archivo1.pdf
│               └── archivo2.png
│
└── tests/                           # Tests unitarios
    ├── __init__.py
    ├── conftest.py                  # Fixtures globales (BD en memoria, TestClient, mocks)
    ├── core/                        # Tests del módulo Core
    │   ├── test_config.py           # Settings, variables de entorno, campos obligatorios
    │   ├── test_database.py         # Engine, sesiones, creación de tablas
    │   ├── test_dependencies.py     # Fábricas de dependencias FastAPI
    │   └── test_logging_config.py   # Configuración de logging
    ├── proyectos/
    │   ├── test_router.py
    │   ├── test_service.py
    │   └── test_repository.py
    ├── tareas/
    │   ├── test_service.py          # Tests de cálculo de tiempo y transiciones de estado
    │   └── test_repository.py
    ├── sincronizacion/
    │   └── test_sincronizador.py    # Tests con mock de Azure DevOps API
    └── tablero/
        └── test_metricas.py
```

---

## Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Módulos | `snake_case` (singular) | `proyectos/`, `tareas/` |
| Clases | `PascalCase` | `ProyectoService`, `TareaRepository` |
| Funciones/variables | `snake_case` | `listar_activos()`, `proyecto_id` |
| Archivos Python | `snake_case` | `router.py`, `service.py` |
| Templates | `snake_case` | `list.html`, `detail.html` |
| Endpoints | `snake_case` plural | `/proyectos`, `/tareas/{id}/archivar` |
