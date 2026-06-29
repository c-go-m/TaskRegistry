"""Esquemas Pydantic para la entidad Proyecto.

Define los contratos de entrada (create, update) y salida (response)
para la API REST y las vistas web del módulo de proyectos.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProyectoCreate(BaseModel):
    """Esquema para crear un nuevo proyecto.

    Attributes:
        nombre: Nombre del proyecto (obligatorio, 1-200 caracteres).
        descripcion: Descripción opcional del proyecto (máximo 2000 caracteres).
    """

    nombre: str = Field(
        min_length=1,
        max_length=200,
        description="Nombre del proyecto",
    )
    descripcion: str = Field(
        default="",
        max_length=2000,
        description="Descripción opcional del proyecto",
    )


class ProyectoUpdate(BaseModel):
    """Esquema para actualizar un proyecto existente.

    Todos los campos son opcionales. Solo se actualizan los campos enviados.

    Attributes:
        nombre: Nuevo nombre del proyecto (1-200 caracteres si se envía).
        descripcion: Nueva descripción del proyecto (máximo 2000 caracteres si se envía).
    """

    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Nombre del proyecto",
    )
    descripcion: str | None = Field(
        default=None,
        max_length=2000,
        description="Descripción del proyecto",
    )


class ProyectoResponse(BaseModel):
    """Esquema de respuesta con los datos completos de un proyecto.

    Attributes:
        id: Identificador único del proyecto.
        nombre: Nombre del proyecto.
        descripcion: Descripción del proyecto.
        activo: Indica si el proyecto está activo.
        created_at: Fecha y hora de creación.
        updated_at: Fecha y hora de última actualización.
    """

    id: int
    nombre: str
    descripcion: str
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
