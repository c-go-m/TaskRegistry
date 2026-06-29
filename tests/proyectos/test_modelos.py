"""Tests para el modelo Proyecto y sus esquemas Pydantic.

RED phase: estos tests deben fallar inicialmente porque modelos.py
y esquemas.py aún no existen.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine

from proyectos.esquemas import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from proyectos.modelos import Proyecto

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Crea un engine SQLite en memoria para los tests."""
    e = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(e)
    return e


@pytest.fixture
def session(engine):
    """Crea una sesión de base de datos para los tests."""
    with Session(engine) as s:
        yield s


# ---------------------------------------------------------------------------
# Tests del modelo Proyecto
# ---------------------------------------------------------------------------


class TestProyectoModel:
    """Suite de tests para el modelo SQLModel Proyecto."""

    def test_crear_proyecto_valores_por_defecto(self, session: Session):
        """Verifica que el modelo se crea con valores por defecto correctos."""
        proyecto = Proyecto(nombre="Test Proyecto")
        session.add(proyecto)
        session.commit()
        session.refresh(proyecto)

        assert proyecto.id is not None
        assert proyecto.nombre == "Test Proyecto"
        assert proyecto.descripcion == ""
        assert proyecto.activo is True
        assert isinstance(proyecto.created_at, datetime)
        assert isinstance(proyecto.updated_at, datetime)

    def test_nombre_es_obligatorio(self):
        """Verifica que nombre es un campo obligatorio sin valor por defecto."""
        # SQLModel table=True: si no se pasa nombre, queda como None
        proyecto = Proyecto()
        assert proyecto.nombre is None

    def test_timestamps_se_asignan_automaticamente(self, session: Session):
        """Verifica que created_at y updated_at se asignan al crear."""
        proyecto = Proyecto(nombre="Timestamps Test")
        session.add(proyecto)
        session.commit()
        session.refresh(proyecto)

        now = datetime.now(UTC)
        assert proyecto.created_at is not None
        assert proyecto.updated_at is not None
        # Los timestamps deben ser recientes (menos de 5 segundos de diferencia)
        assert (now - proyecto.created_at.astimezone(UTC)).total_seconds() < 5
        assert (now - proyecto.updated_at.astimezone(UTC)).total_seconds() < 5

    def test_nombre_tabla_en_bd(self):
        """Verifica el nombre de la tabla en base de datos."""
        assert Proyecto.__tablename__ == "proyectos"

    def test_descripcion_opcional_default_vacio(self, session: Session):
        """Verifica que descripcion por defecto es string vacío."""
        proyecto = Proyecto(nombre="Sin descripción")
        session.add(proyecto)
        session.commit()
        session.refresh(proyecto)

        assert proyecto.descripcion == ""

    def test_activo_default_true(self, session: Session):
        """Verifica que activo por defecto es True."""
        proyecto = Proyecto(nombre="Activo por defecto")
        session.add(proyecto)
        session.commit()
        session.refresh(proyecto)

        assert proyecto.activo is True

    def test_nombre_max_200_caracteres(self):
        """Verifica que nombre tiene un máximo de 200 caracteres en la columna."""
        col = Proyecto.__table__.columns["nombre"]
        assert col.type.length == 200

    def test_descripcion_max_2000_caracteres(self):
        """Verifica que descripcion tiene un máximo de 2000 caracteres en la columna."""
        col = Proyecto.__table__.columns["descripcion"]
        assert col.type.length == 2000


    def test_updated_at_se_actualiza_al_modificar(self, session: Session):
        """Verifica que updated_at cambia cuando se modifica el proyecto."""
        proyecto = Proyecto(nombre="Original")
        session.add(proyecto)
        session.commit()
        session.refresh(proyecto)

        updated_at_original = proyecto.updated_at

        # Modificar el proyecto
        proyecto.nombre = "Modificado"
        session.commit()
        session.refresh(proyecto)

        assert proyecto.updated_at > updated_at_original

    def test_repr_string(self):
        """Verifica la representación en string del modelo."""
        proyecto = Proyecto(nombre="Repr Test")
        assert "Proyecto" in repr(proyecto)
        assert "Repr Test" in repr(proyecto)


# ---------------------------------------------------------------------------
# Tests de esquemas Pydantic
# ---------------------------------------------------------------------------


class TestProyectoCreateSchema:
    """Suite de tests para el schema ProyectoCreate."""

    def test_campos_obligatorios(self):
        """Verifica que nombre es obligatorio en ProyectoCreate."""
        with pytest.raises(ValidationError):
            ProyectoCreate()

    def test_campos_validos(self):
        """Verifica creación con datos válidos."""
        data = ProyectoCreate(nombre="Nuevo Proyecto")
        assert data.nombre == "Nuevo Proyecto"
        assert data.descripcion == ""

    def test_descripcion_opcional(self):
        """Verifica que descripcion es opcional en ProyectoCreate."""
        data = ProyectoCreate(nombre="Proyecto", descripcion="Una descripción")
        assert data.descripcion == "Una descripción"

    def test_nombre_no_vacio(self):
        """Verifica que nombre no puede ser una cadena vacía."""
        with pytest.raises(ValidationError):
            ProyectoCreate(nombre="")


class TestProyectoUpdateSchema:
    """Suite de tests para el schema ProyectoUpdate."""

    def test_todos_campos_opcionales(self):
        """Verifica que todos los campos son opcionales en ProyectoUpdate."""
        data = ProyectoUpdate()
        assert data.nombre is None
        assert data.descripcion is None

    def test_actualizar_nombre(self):
        """Verifica actualización solo de nombre."""
        data = ProyectoUpdate(nombre="Nuevo nombre")
        assert data.nombre == "Nuevo nombre"
        assert data.descripcion is None

    def test_actualizar_descripcion(self):
        """Verifica actualización solo de descripción."""
        data = ProyectoUpdate(descripcion="Nueva descripción")
        assert data.nombre is None
        assert data.descripcion == "Nueva descripción"

    def test_actualizar_todos_campos(self):
        """Verifica actualización de todos los campos."""
        data = ProyectoUpdate(nombre="Nombre", descripcion="Descripción")
        assert data.nombre == "Nombre"
        assert data.descripcion == "Descripción"


class TestProyectoResponseSchema:
    """Suite de tests para el schema ProyectoResponse."""

    def test_campos_completos(self):
        """Verifica que ProyectoResponse tiene todos los campos esperados."""
        data = ProyectoResponse(
            id=1,
            nombre="Proyecto",
            descripcion="Descripción",
            activo=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        assert data.id == 1
        assert data.nombre == "Proyecto"
        assert data.descripcion == "Descripción"
        assert data.activo is True
        assert isinstance(data.created_at, datetime)
        assert isinstance(data.updated_at, datetime)

    def test_from_attributes(self):
        """Verifica que ProyectoResponse puede crearse desde atributos de modelo."""
        data = ProyectoResponse(
            id=2,
            nombre="From Model",
            descripcion="Test",
            activo=False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        assert data.model_config.get("from_attributes") is True
