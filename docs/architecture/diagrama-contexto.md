# Diagrama de Contexto (C4 Nivel 1)

> Muestra el sistema TaskRegistry y sus interacciones con actores y sistemas externos.

```mermaid
C4Context
    title "Diagrama de Contexto — TaskRegistry"

    Person(usuario, "Usuario Profesional", "Único usuario que registra tareas y consulta métricas")

    System_Boundary(taskregistry, "TaskRegistry") {
        System(app, "TaskRegistry App", "Bitácora personal de tareas con control de tiempo y sincronización Azure DevOps")
    }

    System_Ext(azure_devops, "Azure DevOps", "Plataforma de gestión de proyectos. Almacena Work Items (Tasks) vinculados a HU")
    System_Ext(sistema_archivos, "Sistema de Archivos Local", "Almacena documentos adjuntos y archivos de configuración")

    Rel(usuario, app, "1. Gestiona proyectos, tareas y documentos", "HTTP (localhost:8080)")
    Rel(usuario, app, "2. Consulta métricas en tablero", "HTTP")
    Rel(usuario, app, "3. Inicia sincronización semanal", "HTTP")

    Rel(app, azure_devops, "Crea Work Items (Tasks) vía REST API", "HTTPS / PAT")
    Rel(app, sistema_archivos, "Lee/escribe archivos adjuntos y BD SQLite", "I/O local")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Descripción de elementos

| Elemento | Descripción |
|----------|-------------|
| **Usuario Profesional** | Actor único. Usuario técnico que opera la app localmente. No hay autenticación ni roles. |
| **TaskRegistry App** | Sistema principal. Servidor web Python (FastAPI) corriendo en localhost. Sirve HTML con Jinja2 + HTMX + Alpine.js. |
| **Azure DevOps** | Sistema externo. Recibe tareas vía REST API para crear Work Items de tipo Task. |
| **Sistema de Archivos Local** | Almacenamiento local de la BD SQLite y los archivos adjuntos de documentos. |

## Flujo principal

1. El usuario accede desde el navegador a `http://localhost:8080`
2. Gestiona proyectos, registra tareas con tiempos y adjunta documentación
3. Al final de la semana, selecciona tareas en estado `Ejecutada` e inicia sincronización
4. La app crea Work Items en Azure DevOps y marca las tareas como `Sincronizada`
5. El tablero de control muestra métricas agregadas por proyecto y rango de fechas
