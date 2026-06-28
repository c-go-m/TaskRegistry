# Diagrama de Contenedores (C4 Nivel 2)

> Muestra los contenedores (aplicaciones, bases de datos, etc.) dentro del sistema TaskRegistry y sus interacciones.

```mermaid
C4Container
    title "Diagrama de Contenedores — TaskRegistry"

    Person(usuario, "Usuario Profesional", "Único usuario", "Navegador web")

    System_Boundary(app, "TaskRegistry App") {
        Container(web_app, "Aplicación Web", "FastAPI + Jinja2 + HTMX + Alpine.js", "Servidor Python que sirve HTML, CSS, JS y expone API REST")
        Container(db, "Base de Datos", "SQLite (SQLModel)", "Almacena proyectos, tareas, documentos y configuración de Azure DevOps")
        Container(files, "Almacenamiento Local", "Sistema de Archivos", "Guarda archivos adjuntos en data/docs/{proyecto}/{documento}/")
        Container(logs, "Archivo de Logs", "Texto (logging)", "Registro de actividad en data/taskregistry.log")
    }

    Container_Ext(azure_api, "Azure DevOps REST API", "Sistema Externo", "Endpoint: POST /_apis/wit/workitems/$Task")

    Rel(usuario, web_app, "Navega y opera la app", "HTTP (localhost:8080)")
    Rel(web_app, db, "Lee y escribe datos", "SQLAlchemy / SQLModel", "SQL")
    Rel(web_app, files, "Guarda y recupera archivos", "I/O local", "Lectura/Escritura")
    Rel(web_app, logs, "Registra eventos", "logging", "Texto")
    Rel(web_app, azure_api, "Crea Work Items", "HTTPS + PAT", "JSON Patch")
```

## Detalle de contenedores

### Aplicación Web (FastAPI)
| Aspecto | Descripción |
|---------|-------------|
| Puerto | `8080` (localhost) |
| Templates | Jinja2 con layouts reutilizables |
| Interactividad | HTMX para actualizaciones parciales, Alpine.js para estado local |
| Endpoints | RESTful, documentados automáticamente en `/docs` (Swagger) |
| Dependencias principales | `fastapi`, `uvicorn`, `sqlmodel`, `httpx` (para Azure API), `python-multipart` (para subida archivos) |

### Base de Datos (SQLite)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | `data/taskregistry.db` |
| Tablas | `proyectos`, `tareas`, `documentos`, `archivos_adjuntos`, `configuracion_azure` |
| Migraciones | Alembic (vía SQLModel) |
| Backup | Copiar el archivo `.db` |

### Almacenamiento Local (Archivos)
| Aspecto | Descripción |
|---------|-------------|
| Ruta base | `data/docs/` |
| Estructura | `{proyecto_id}/{documento_id}/{archivo}` |
| Límite | 50 MB por archivo (MVP) |

## Flujo de sincronización (secuencia)

```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web App (FastAPI)
    participant DB as SQLite
    participant AZ as Azure DevOps API

    U->>W: POST /sincronizacion/sync (tareas_ids, hu_id)
    W->>DB: Consultar tareas seleccionadas
    DB-->>W: Lista de tareas en estado "Ejecutada"
    loop Por cada tarea
        W->>AZ: POST /workitems/$Task (JSON Patch)
        alt Éxito
            AZ-->>W: 201 Created (WorkItem ID: 12345)
            W->>DB: Actualizar id_azure_devops, estado="Sincronizada"
        else Error
            AZ-->>W: 4xx/5xx
            W->>DB: Registrar error (tarea queda en "Ejecutada")
        end
    end
    W-->>U: Resumen: N tareas sincronizadas, M fallos
```

## Distribución física

```
Máquina local (Windows)
│
├── 🖥️  Navegador (Chrome/Edge/Firefox)
│
└── 🐍 Python 3.12+
    └── TaskRegistry App (FastAPI en localhost:8080)
        ├── 📄 data/taskregistry.db       (SQLite)
        ├── 📁 data/docs/                 (Archivos adjuntos)
        └── 📄 data/taskregistry.log      (Logs)
```
