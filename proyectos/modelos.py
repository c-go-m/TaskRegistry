"""Modelo SQLModel para la entidad Proyecto."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Proyecto(SQLModel, table=True):
    """Representa un proyecto en el sistema.

    Proyecto es la unidad organizadora de tareas. Cada proyecto tiene un nombre
    obligatorio, una descripción opcional y soporta soft-delete mediante el
    campo ``activo``.

    Attributes:
        id: Identificador único autogenerado.
        nombre: Nombre del proyecto (obligatorio, máximo 200 caracteres).
        descripcion: Descripción opcional del proyecto (máximo 2000 caracteres).
        activo: Indica si el proyecto está activo (soft-delete). Default True.
        created_at: Marca de tiempo de creación (se asigna automáticamente).
        updated_at: Marca de tiempo de última modificación (se actualiza automáticamente).
    """

    __tablename__: str = "proyectos"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(
        index=True,
        max_length=200,
        min_length=1,
        nullable=False,
    )
    descripcion: str = Field(default="", max_length=2000)
    activo: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
        nullable=False,
    )
