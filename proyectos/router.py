"""Routers API REST y Web para el módulo de proyectos.

Define dos routers separados:
- ``router_api``: Endpoints JSON para operaciones CRUD.
- ``router_web``: Rutas HTML con Jinja2 + HTMX.
"""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from core.dependencies import get_db
from proyectos.esquemas import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from proyectos.repositorio import ProyectoRepository
from proyectos.servicios import ProyectoService

# ---------------------------------------------------------------------------
# Jinja2 Templates
# ---------------------------------------------------------------------------

_templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(_templates_dir))

# ---------------------------------------------------------------------------
# Router API REST
# ---------------------------------------------------------------------------

router_api = APIRouter(prefix="/api/proyectos", tags=["Proyectos API"])


def get_proyecto_service(session: Session = Depends(get_db)) -> ProyectoService:
    """Dependencia que provee un ProyectoService con su repositorio inyectado.

    Args:
        session: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Instancia de ProyectoService lista para usar.
    """
    repo = ProyectoRepository(session)
    return ProyectoService(repositorio=repo)


@router_api.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def crear_proyecto(
    data: ProyectoCreate,
    service: ProyectoService = Depends(get_proyecto_service),
) -> ProyectoResponse:
    """Crea un nuevo proyecto.

    Args:
        data: Datos del proyecto a crear.
        service: Servicio de proyectos inyectado.

    Returns:
        Proyecto creado con ID y timestamps asignados.
    """
    proyecto = service.crear(data)
    return ProyectoResponse.model_validate(proyecto)


@router_api.get("/", response_model=list[ProyectoResponse])
def listar_proyectos(
    service: ProyectoService = Depends(get_proyecto_service),
) -> list[ProyectoResponse]:
    """Lista todos los proyectos activos.

    Args:
        service: Servicio de proyectos inyectado.

    Returns:
        Lista de proyectos activos ordenados por fecha de creación descendente.
    """
    proyectos = service.listar_activos()
    return [ProyectoResponse.model_validate(p) for p in proyectos]


@router_api.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener_proyecto(
    proyecto_id: int,
    service: ProyectoService = Depends(get_proyecto_service),
) -> ProyectoResponse:
    """Obtiene un proyecto por su ID.

    Args:
        proyecto_id: Identificador del proyecto.
        service: Servicio de proyectos inyectado.

    Returns:
        Proyecto solicitado.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    proyecto = service.obtener_por_id(proyecto_id)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    return ProyectoResponse.model_validate(proyecto)


@router_api.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto(
    proyecto_id: int,
    data: ProyectoUpdate,
    service: ProyectoService = Depends(get_proyecto_service),
) -> ProyectoResponse:
    """Actualiza un proyecto existente.

    Args:
        proyecto_id: Identificador del proyecto a actualizar.
        data: Datos a actualizar (solo campos enviados).
        service: Servicio de proyectos inyectado.

    Returns:
        Proyecto actualizado.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    proyecto = service.actualizar(proyecto_id, data)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    return ProyectoResponse.model_validate(proyecto)


@router_api.patch("/{proyecto_id}/archivar", response_model=ProyectoResponse)
def archivar_proyecto(
    proyecto_id: int,
    service: ProyectoService = Depends(get_proyecto_service),
) -> ProyectoResponse:
    """Archiva (soft-delete) un proyecto.

    Args:
        proyecto_id: Identificador del proyecto a archivar.
        service: Servicio de proyectos inyectado.

    Returns:
        Proyecto archivado con activo=False.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    proyecto = service.archivar(proyecto_id)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    return ProyectoResponse.model_validate(proyecto)


# ---------------------------------------------------------------------------
# Router Web (Jinja2 + HTMX)
# ---------------------------------------------------------------------------

router_web = APIRouter(prefix="/proyectos", tags=["Proyectos Web"])


def _get_web_service(session: Session = Depends(get_db)) -> ProyectoService:
    """Dependencia que provee un ProyectoService para las vistas web.

    Args:
        session: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Instancia de ProyectoService lista para usar.
    """
    repo = ProyectoRepository(session)
    return ProyectoService(repositorio=repo)


@router_web.get("/")
def listar_proyectos_web(
    request: Request,
    q: str = "",
    archivados: bool = False,
    service: ProyectoService = Depends(_get_web_service),
):
    """Página HTML con la lista de proyectos.

    Soporta búsqueda por nombre (``q``) y visualización de proyectos
    archivados (``archivados``). Los filtros se aplican del lado del
    servidor cuando se proporcionan parámetros, o del lado del cliente
    (JS) para respuestas HTMX parciales.

    Si la petición viene de HTMX (``HX-Request`` header), retorna solo el
    partial del grid para evitar duplicar el layout al hacer swap
    dentro de ``#main-content``.

    Args:
        request: Objeto Request de FastAPI.
        q: Término de búsqueda por nombre (opcional).
        archivados: Si es True, incluye proyectos archivados.
        service: Servicio de proyectos inyectado.

    Returns:
        Plantilla HTML renderizada con el grid de proyectos.
    """
    if archivados:
        proyectos = service.listar_todos()
    else:
        proyectos = service.listar_activos()

    if q:
        q_lower = q.lower()
        proyectos = [p for p in proyectos if q_lower in p.nombre.lower()]

    template_name = (
        "proyectos/_project_grid_container.html"
        if request.headers.get("hx-request") == "true"
        else "proyectos/list.html"
    )
    return templates.TemplateResponse(
        request,
        template_name,
        {"proyectos": proyectos},
    )


@router_web.get("/nuevo")
def nuevo_proyecto_form(
    request: Request,
):
    """Formulario HTML para crear un nuevo proyecto.

    Args:
        request: Objeto Request de FastAPI.

    Returns:
        Plantilla HTML con el formulario de creación.
    """
    return templates.TemplateResponse(
        request,
        "proyectos/form.html",
        {"proyecto": None},
    )


@router_web.post("/")
def crear_proyecto_web(
    request: Request,
    nombre: str = Form(..., min_length=1, max_length=200),
    descripcion: str = Form(default="", max_length=2000),
    service: ProyectoService = Depends(_get_web_service),
):
    """Crea un proyecto desde formulario HTMX.

    Args:
        request: Objeto Request de FastAPI.
        nombre: Nombre del proyecto.
        descripcion: Descripción opcional del proyecto.
        service: Servicio de proyectos inyectado.

    Returns:
        Partial HTML de la tabla de proyectos actualizada.

    Raises:
        HTTPException 422: Si los datos de entrada no son válidos.
    """
    data = ProyectoCreate(nombre=nombre, descripcion=descripcion)
    service.crear(data)
    proyectos = service.listar_activos()
    return templates.TemplateResponse(
        request,
        "proyectos/_project_grid_container.html",
        {"proyectos": proyectos},
    )


@router_web.get("/{proyecto_id}/editar")
def editar_proyecto_form(
    request: Request,
    proyecto_id: int,
    service: ProyectoService = Depends(_get_web_service),
):
    """Formulario HTML precargado para editar un proyecto.

    Args:
        request: Objeto Request de FastAPI.
        proyecto_id: Identificador del proyecto a editar.
        service: Servicio de proyectos inyectado.

    Returns:
        Plantilla HTML con el formulario precargado.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    proyecto = service.obtener_por_id(proyecto_id)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    return templates.TemplateResponse(
        request,
        "proyectos/form.html",
        {"proyecto": proyecto},
    )


@router_web.put("/{proyecto_id}")
def actualizar_proyecto_web(
    request: Request,
    proyecto_id: int,
    nombre: str = Form(..., min_length=1, max_length=200),
    descripcion: str = Form(default="", max_length=2000),
    service: ProyectoService = Depends(_get_web_service),
):
    """Actualiza un proyecto desde formulario HTMX.

    Args:
        request: Objeto Request de FastAPI.
        proyecto_id: Identificador del proyecto a actualizar.
        nombre: Nuevo nombre del proyecto.
        descripcion: Nueva descripción del proyecto.
        service: Servicio de proyectos inyectado.

    Returns:
        Partial HTML de la tabla de proyectos actualizada.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    data = ProyectoUpdate(nombre=nombre, descripcion=descripcion)
    proyecto = service.actualizar(proyecto_id, data)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    proyectos = service.listar_activos()
    return templates.TemplateResponse(
        request,
        "proyectos/_project_grid_container.html",
        {"proyectos": proyectos},
    )


@router_web.patch("/{proyecto_id}/archivar")
def archivar_proyecto_web(
    request: Request,
    proyecto_id: int,
    service: ProyectoService = Depends(_get_web_service),
):
    """Archiva (soft-delete) un proyecto desde HTMX.

    Args:
        request: Objeto Request de FastAPI.
        proyecto_id: Identificador del proyecto a archivar.
        service: Servicio de proyectos inyectado.

    Returns:
        Partial HTML de la tabla de proyectos actualizada.

    Raises:
        HTTPException 404: Si el proyecto no existe.
    """
    proyecto = service.archivar(proyecto_id)
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id {proyecto_id} no encontrado",
        )
    proyectos = service.listar_activos()
    return templates.TemplateResponse(
        request,
        "proyectos/_project_grid.html",
        {"proyectos": proyectos},
    )
