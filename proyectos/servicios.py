"""Servicio CRUD para la entidad Proyecto.

Define la lógica de negocio para crear, listar, obtener, actualizar
y archivar proyectos. El servicio recibe un ``ProyectoRepository``
inyectado para separar la lógica de negocio del acceso a datos.
"""

import logging
from datetime import UTC, datetime

from proyectos.esquemas import ProyectoCreate, ProyectoUpdate
from proyectos.modelos import Proyecto
from proyectos.repositorio import ProyectoRepository

logger = logging.getLogger(__name__)


class ProyectoService:
    """Servicio de operaciones CRUD para proyectos.

    Args:
        repositorio: Instancia de ProyectoRepository para acceso a datos.
    """

    def __init__(self, repositorio: ProyectoRepository) -> None:
        """Inicializa el servicio con un repositorio inyectado.

        Args:
            repositorio: Repositorio de proyectos para acceso a base de datos.
        """
        self._repo = repositorio

    def crear(self, data: ProyectoCreate) -> Proyecto:
        """Crea un nuevo proyecto.

        Args:
            data: Datos validados del proyecto a crear.

        Returns:
            Proyecto persistido con su ID y timestamps asignados.
        """
        proyecto = Proyecto(
            nombre=data.nombre,
            descripcion=data.descripcion,
        )
        resultado = self._repo.add(proyecto)
        logger.info("Proyecto creado: id=%d nombre='%s'", resultado.id, resultado.nombre)
        return resultado

    def listar_todos(self) -> list[Proyecto]:
        """Lista todos los proyectos, incluyendo archivados.

        Returns:
            Lista completa de proyectos ordenados por ``created_at`` descendente.
        """
        return self._repo.list_all()

    def listar_activos(self) -> list[Proyecto]:
        """Lista todos los proyectos activos.

        Returns:
            Lista de proyectos con ``activo=True`` ordenados por
            ``created_at`` descendente.
        """
        return self._repo.list_activos()

    def obtener_por_id(self, proyecto_id: int) -> Proyecto | None:
        """Obtiene un proyecto por su ID.

        Args:
            proyecto_id: Identificador único del proyecto.

        Returns:
            Proyecto si existe, None en caso contrario.
        """
        return self._repo.get(proyecto_id)

    def actualizar(
        self,
        proyecto_id: int,
        data: ProyectoUpdate,
    ) -> Proyecto | None:
        """Actualiza los campos enviados de un proyecto existente.

        Solo se actualizan los campos que no son ``None`` en ``data``.
        El campo ``updated_at`` se actualiza automáticamente.

        Args:
            proyecto_id: Identificador del proyecto a actualizar.
            data: Datos a actualizar (solo campos no-None se aplican).

        Returns:
            Proyecto actualizado si existe, None si no se encuentra.
        """
        proyecto = self._repo.get(proyecto_id)
        if proyecto is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(proyecto, field, value)

        proyecto.updated_at = datetime.now(UTC)
        resultado = self._repo.save(proyecto)
        logger.info(
            "Proyecto actualizado: id=%d campos=%s",
            proyecto_id,
            list(update_data.keys()),
        )
        return resultado

    def archivar(self, proyecto_id: int) -> Proyecto | None:
        """Archiva (soft-delete) un proyecto.

        Establece ``activo=False`` y actualiza ``updated_at``.

        Args:
            proyecto_id: Identificador del proyecto a archivar.

        Returns:
            Proyecto archivado si existe, None si no se encuentra.
        """
        proyecto = self._repo.get(proyecto_id)
        if proyecto is None:
            return None

        proyecto.activo = False
        proyecto.updated_at = datetime.now(UTC)
        resultado = self._repo.save(proyecto)
        logger.info("Proyecto archivado: id=%d", proyecto_id)
        return resultado
