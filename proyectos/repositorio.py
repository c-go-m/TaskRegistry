"""Repositorio para la entidad Proyecto.

Capa de acceso a datos que abstrae las operaciones de base de datos
del modelo Proyecto. El repositorio trabaja directamente con objetos
``Proyecto`` y delega en SQLModel/SQLAlchemy para la persistencia.
"""

from sqlmodel import Session, select

from proyectos.modelos import Proyecto


class ProyectoRepository:
    """Repositorio para operaciones de base de datos de Proyecto.

    Encapsula las consultas y persistencia del modelo ``Proyecto``,
    proporcionando una interfaz limpia para la capa de servicio.

    Args:
        session: Sesión de SQLModel para interactuar con la base de datos.
    """

    def __init__(self, session: Session) -> None:
        """Inicializa el repositorio con una sesión de base de datos.

        Args:
            session: Sesión de SQLModel.
        """
        self._session = session

    def add(self, proyecto: Proyecto) -> Proyecto:
        """Persiste un nuevo proyecto en base de datos.

        Args:
            proyecto: Instancia de Proyecto a persistir (sin ID).

        Returns:
            Proyecto con ID asignado y timestamps actualizados.
        """
        self._session.add(proyecto)
        self._session.commit()
        self._session.refresh(proyecto)
        return proyecto

    def get(self, proyecto_id: int) -> Proyecto | None:
        """Obtiene un proyecto por su ID.

        Args:
            proyecto_id: Identificador único del proyecto.

        Returns:
            Proyecto si existe (incluso archivado), None en caso contrario.
        """
        return self._session.get(Proyecto, proyecto_id)

    def list_activos(self) -> list[Proyecto]:
        """Lista todos los proyectos activos ordenados por fecha de creación descendente.

        Returns:
            Lista de proyectos con ``activo=True`` ordenados por
            ``created_at`` descendente.
        """
        statement = (
            select(Proyecto)
            .where(Proyecto.activo.is_(True))
            .order_by(Proyecto.created_at.desc())
        )
        result = self._session.exec(statement)
        return list(result.all())

    def list_all(self) -> list[Proyecto]:
        """Lista todos los proyectos (activos y archivados) ordenados por created_at descendente.

        Returns:
            Lista completa de proyectos ordenados por ``created_at`` descendente.
        """
        statement = select(Proyecto).order_by(Proyecto.created_at.desc())
        result = self._session.exec(statement)
        return list(result.all())

    def save(self, proyecto: Proyecto) -> Proyecto:
        """Persiste los cambios de un proyecto existente.

        Args:
            proyecto: Instancia de Proyecto con las modificaciones aplicadas.

        Returns:
            Proyecto con los datos actualizados desde base de datos.
        """
        self._session.commit()
        self._session.refresh(proyecto)
        return proyecto
