# Sprint 1 — Módulo Proyectos (CRUD)

> **Proyecto:** TaskRegistry
> **Sprint:** 1
> **Duración estimada:** 1 sesión
> **Objetivo:** Implementar el CRUD completo del módulo de proyectos con API REST y vistas web (Jinja2 + HTMX), siguiendo TDD.

---

## Tareas del Sprint 1

| # | Tarea | Descripción | Archivos a crear/modificar |
|---|-------|-------------|---------------------------|
| 1 | ✅ **Modelo y esquemas** — Completada el 2026-06-28 | Definir modelo SQLModel `Proyecto` + schemas Pydantic de entrada/salida | `proyectos/modelos.py`, `proyectos/esquemas.py`, `tests/proyectos/test_modelos.py` |
| 2 | ✅ **Servicio CRUD** — Completada el 2026-06-28 | Implementar capa de servicios + **Repository pattern**. `ProyectoService` recibe `ProyectoRepository` inyectado (DI). | `proyectos/servicios.py`, `proyectos/repositorio.py`, `tests/proyectos/test_servicios.py`, `tests/proyectos/test_repositorio.py` |
| 3 | ✅ **Router API REST** — Completada el 2026-06-28 | Endpoints JSON: POST, GET (lista), GET (detalle), PUT, PATCH (archivar) | `proyectos/router.py`, `tests/proyectos/test_router_api.py` |
| 4 | ✅ **Vistas Web (Jinja2 + HTMX)** — Completada el 2026-06-28 | Templates HTML para listar, crear, editar y archivar proyectos con HTMX | `proyectos/templates/proyectos/list.html`, `proyectos/templates/proyectos/_tabla.html`, `proyectos/templates/proyectos/form.html`, `static/css/estilos.css`, `tests/proyectos/test_web.py` |
| 5 | ✅ **Integración en la app** — Completada el 2026-06-28 | Registrar el router en `main.py`, verificar Swagger UI y humo test | `main.py` (modificar) |

---

## Tarea 1: Modelo y esquemas

### Archivos a crear
- `proyectos/modelos.py`
- `proyectos/esquemas.py`
- `tests/proyectos/test_modelos.py`

### Que debe implementarse

**modelos.py**: Clase `Proyecto` (SQLModel, table=True) con los campos:
- `id`: int, primary key, autogenerado
- `nombre`: str, indexado, obligatorio, máx 200 caracteres
- `descripcion`: str, opcional (default ""), máx 2000 caracteres
- `activo`: bool, default True (para soft delete)
- `created_at`: datetime, se asigna automáticamente al crear
- `updated_at`: datetime, se actualiza automáticamente al modificar
- `__tablename__`: "proyectos"

**esquemas.py**: Schemas Pydantic:
- `ProyectoCreate`: nombre (obligatorio), descripcion (opcional)
- `ProyectoUpdate`: nombre (opcional), descripcion (opcional)
- `ProyectoResponse`: id, nombre, descripcion, activo, created_at, updated_at (con `from_attributes=True`)

### Tests TDD requeridos (RED -> GREEN -> REFACTOR)
- Verificar que el modelo se crea con valores por defecto correctos
- Verificar que nombre es obligatorio
- Verificar que los timestamps se asignan automáticamente
- Verificar el nombre de la tabla en BD

### Verificación
```powershell
pytest tests/proyectos/test_modelos.py -v
ruff check proyectos/modelos.py proyectos/esquemas.py
```

---

## Tarea 2: Servicio CRUD

### Archivos a crear
- `proyectos/servicios.py`
- `tests/proyectos/test_servicios.py`

### Que debe implementarse

**servicios.py**: Clase `ProyectoService` que recibe una `Session` de SQLModel y expone:
- `crear(data: ProyectoCreate) -> Proyecto`: crea, persiste y retorna el proyecto
- `listar_activos() -> list[Proyecto]`: retorna proyectos con activo=True, ordenados por created_at descendente
- `obtener_por_id(proyecto_id: int) -> Proyecto | None`: busca por ID
- `actualizar(proyecto_id: int, data: ProyectoUpdate) -> Proyecto | None`: actualiza solo los campos enviados, actualiza updated_at
- `archivar(proyecto_id: int) -> Proyecto | None`: soft delete (activo = False), actualiza updated_at

### Tests TDD requeridos
- Crear proyecto válido con y sin descripción
- Listar solo proyectos activos (excluye archivados)
- Lista vacía cuando no hay proyectos
- Obtener proyecto por ID existente e inexistente (retorna None)
- Actualizar nombre de proyecto existente
- Actualizar proyecto inexistente retorna None
- Archivar proyecto cambia activo a False
- Archivar proyecto inexistente retorna None

### Verificación
```powershell
pytest tests/proyectos/test_servicios.py -v
ruff check proyectos/servicios.py
```

---

## Tarea 3: Router API REST

### Archivos a crear
- `proyectos/router.py` (contiene tanto router_api como router_web)
- `tests/proyectos/test_router_api.py`

### Que debe implementarse

**router.py** — Dos routers separados:

1. `router_api = APIRouter(prefix="/api/proyectos", tags=["Proyectos API"])` con:
   - `POST /`: crear proyecto, status code 201
   - `GET /`: listar proyectos activos
   - `GET /{proyecto_id}`: obtener detalle (404 si no existe)
   - `PUT /{proyecto_id}`: actualizar proyecto (404 si no existe)
   - `PATCH /{proyecto_id}/archivar`: archivar proyecto (404 si no existe)

2. `router_web = APIRouter(prefix="/proyectos", tags=["Proyectos Web"])` con:
   - `GET /`: página HTML con lista de proyectos
   - `GET /nuevo`: formulario HTML para crear
   - `POST /`: crear proyecto desde formulario (HTMX)
   - `GET /{proyecto_id}/editar`: formulario HTML precargado
   - `PUT /{proyecto_id}`: actualizar desde formulario (HTMX)
   - `PATCH /{proyecto_id}/archivar`: archivar desde web (HTMX)

Ambos routers usan `ProyectoService` con la sesión de BD inyectada vía `Depends(get_db)`.

### Tests TDD requeridos (API REST)
- Crear proyecto retorna 201 con datos correctos
- Crear proyecto sin nombre retorna 422
- Listar proyectos retorna lista con proyectos creados
- Listar sin proyectos retorna lista vacía
- Obtener proyecto existente retorna 200 con datos
- Obtener proyecto inexistente retorna 404
- Actualizar proyecto existente retorna 200 con datos modificados
- Actualizar proyecto inexistente retorna 404
- Archivar proyecto existente retorna 200 con activo=False
- Archivar proyecto inexistente retorna 404

### Verificación
```powershell
pytest tests/proyectos/test_router_api.py -v
# Abrir http://localhost:8000/docs — deben aparecer los 5 endpoints de proyectos
```

---

## Tarea 4: Vistas Web (Jinja2 + HTMX)

### Archivos a crear
- `proyectos/templates/proyectos/list.html`
- `proyectos/templates/proyectos/_tabla.html`
- `proyectos/templates/proyectos/form.html`
- `static/css/estilos.css`
- `tests/proyectos/test_web.py`

### Que debe implementarse

**list.html**: Página principal con:
- Header con título "Proyectos" y botón "Nuevo Proyecto" (HTMX)
- `div#tabla-proyectos` que incluye el partial `_tabla.html`
- Script HTMX desde CDN
- CSS básico incluido

**_tabla.html**: Partial HTML que se actualiza vía HTMX:
- Tabla con columnas: ID, Nombre, Descripción (truncada a 50 chars), Creado, Acciones
- Botón "Editar" que carga formulario vía HTMX en `#main-content`
- Botón "Archivar" con confirmación, que actualiza `#tabla-proyectos` vía HTMX
- Mensaje "No hay proyectos activos" cuando la lista está vacía

**form.html**: Formulario único para crear y editar:
- Si `proyecto` existe: `hx-put="/proyectos/{id}"` (edición)
- Si `proyecto` es None: `hx-post="/proyectos/"` (creación)
- Campos: nombre (obligatorio), descripción (textarea)
- Botón submit con texto dinámico "Crear" / "Actualizar"
- Botón "Cancelar" que vuelve a la lista vía HTMX

**estilos.css**: Estilos base de la aplicación:
- Layout: fuente system-ui, fondo claro, contenido centrado a 1200px
- Botones: .btn, .btn-primary, .btn-secondary, .btn-danger, .btn-small
- Tabla: .tabla con bordes, hover en filas, sombra suave
- Formulario: .form-proyecto con campos apilados, max-width 600px
- Empty state: mensaje centrado para lista vacía

### Tests TDD requeridos (Web)
- `GET /proyectos/` retorna HTML (content-type text/html)
- `GET /proyectos/` sin proyectos muestra mensaje de empty state
- `GET /proyectos/nuevo` renderiza formulario con texto "Crear"
- `GET /proyectos/999/editar` retorna 404 si el proyecto no existe

### Verificación
```powershell
pytest tests/proyectos/test_web.py -v
# Arrancar app y abrir http://localhost:8000/proyectos/
```

---

## Tarea 5: Integración en la app

### Archivos a modificar
- `main.py`

### Que debe implementarse

Agregar en `main.py`:
- Import de `router_api` y `router_web` desde `proyectos.router`
- Registro de ambos routers con `app.include_router()` antes del return

### Verificación final
```powershell
ruff check . --fix
ruff format . --check
pytest -v --cov=proyectos --cov=core
python run.py
# Abrir:
# - http://localhost:8000/docs          (Swagger UI con endpoints)
# - http://localhost:8000/api/proyectos/ (JSON)
# - http://localhost:8000/proyectos/     (Interfaz web)
```

---

## Criterios de aceptación del Sprint 1

### Criterios generales (DoD)
- [x] **TDD**: Cada tarea de código siguió RED -> GREEN -> REFACTOR
- [x] **Tests**: Todos los tests pasan con `pytest -v` (94 tests)
- [x] **Ruff**: `ruff check .` pasa sin errores
- [ ] **Commits**: Todos siguen Conventional Commits (`feat:`, `test:`, `refactor:`, etc.)
- [x] **Cobertura**: Las nuevas líneas de código tienen test asociado

### Criterios funcionales — Modulo Proyectos

| # | Criterio | Verificacion |
|---|----------|--------------|
| 1 | **Crear proyecto** | `POST /api/proyectos/` retorna 201 con el proyecto creado |
| 2 | **Listar proyectos activos** | `GET /api/proyectos/` retorna solo proyectos con activo=True |
| 3 | **Obtener detalle** | `GET /api/proyectos/{id}` retorna el proyecto si existe, 404 si no |
| 4 | **Actualizar proyecto** | `PUT /api/proyectos/{id}` actualiza campos y retorna el proyecto modificado |
| 5 | **Archivar proyecto** | `PATCH /api/proyectos/{id}/archivar` cambia activo a False |
| 6 | ✅ **Vista web lista** | `GET /proyectos/` retorna HTML con tabla de proyectos |
| 7 | ✅ **Vista web formulario** | `GET /proyectos/nuevo` retorna HTML con formulario |
| 8 | ✅ **Vista web editar** | `GET /proyectos/{id}/editar` retorna formulario precargado |
| 9 | ✅ **HTMX crear** | `POST /proyectos/` via HTMX actualiza la tabla sin recargar pagina |
| 10 | ✅ **HTMX archivar** | `PATCH /proyectos/{id}/archivar` via HTMX actualiza la tabla |

---

## Resumen de archivos creados/modificados en Sprint 1

| Archivo | Proposito |
|---------|-----------|
| `proyectos/modelos.py` | Modelo SQLModel `Proyecto` |
| `proyectos/esquemas.py` | Schemas Pydantic (Create, Update, Response) |
| `proyectos/servicios.py` | Capa de servicio CRUD |
| `proyectos/repositorio.py` | Capa de acceso a datos (Repository pattern) |
| `proyectos/router.py` | Endpoints API REST + Rutas Web (Jinja2/HTMX) |
| `proyectos/templates/proyectos/list.html` | Pagina principal de proyectos |
| `proyectos/templates/proyectos/_tabla.html` | Partial HTMX para la tabla |
| `proyectos/templates/proyectos/form.html` | Formulario crear/editar |
| `static/css/estilos.css` | Estilos base de la aplicacion |
| `tests/proyectos/test_modelos.py` | Tests del modelo Proyecto |
| `tests/proyectos/test_servicios.py` | Tests del servicio CRUD |
| `tests/proyectos/test_repositorio.py` | Tests del repositorio |
| `tests/proyectos/test_router_api.py` | Tests de los endpoints REST |
| `tests/proyectos/test_web.py` | Tests de las vistas web |
| `main.py` | **MODIFICADO**: registro de routers de proyectos |

---

## Orden de implementacion sugerido

1. **Tarea 1** -> Modelo y esquemas (sin dependencias)
2. **Tarea 2** -> Servicio CRUD (depende de Tarea 1)
3. **Tarea 3** -> Router API REST (depende de Tarea 2)
4. **Tarea 4** -> Vistas Web (depende de Tarea 2)
5. **Tarea 5** -> Integracion (depende de Tareas 3 y 4)

Cada tarea sigue el ciclo **RED -> GREEN -> REFACTOR**:
1. Escribir los tests primero (RED) -> ver que fallan
2. Implementar el codigo minimo (GREEN) -> ver que pasan
3. Refactorizar si es necesario (REFACTOR) -> tests siguen verdes

---

## Notas de diseno

- **Soft delete**: Se usa el campo `activo` en lugar de DELETE fisico. Los proyectos archivados no se muestran en la lista principal pero persisten en BD.
- **Separacion API/Web**: `/api/proyectos/` para REST JSON, `/proyectos/` para HTML. Ambos comparten la misma capa de servicio.
- **HTMX**: Las interacciones web (crear, editar, archivar) usan HTMX para actualizar solo la tabla sin recargar la pagina completa.
- **TDD obligatorio**: No se escribe codigo de logica sin antes tener el test que falla (RED).
- **Formularios**: Se usa `hx-post` para creacion y `hx-put` para edicion. Los datos se envian como form data estandar y se reciben con `Form(...)` en FastAPI.
