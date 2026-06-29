"""Tests para el servicio CRUD de Proyecto.

RED phase: estos tests deben fallar inicialmente porque servicios.py
aún no existe.
"""

from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine

from proyectos.esquemas import ProyectoCreate, ProyectoUpdate
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


@pytest.fixture
def repo(session):
    """Crea una instancia de ProyectoRepository con la sesión de prueba."""
    from proyectos.repositorio import ProyectoRepository

    return ProyectoRepository(session)


@pytest.fixture
def service(repo):
    """Crea una instancia de ProyectoService con el repositorio inyectado."""
    from proyectos.servicios import ProyectoService

    return ProyectoService(repositorio=repo)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCrearProyecto:
    """Tests para la operación crear del servicio."""

    def test_crear_proyecto_con_descripcion(self, service, session):
        """Verifica crear un proyecto válido con descripción."""
        data = ProyectoCreate(nombre="Mi Proyecto", descripcion="Una descripción")
        proyecto = service.crear(data)

        assert proyecto.id is not None
        assert proyecto.nombre == "Mi Proyecto"
        assert proyecto.descripcion == "Una descripción"
        assert proyecto.activo is True
        assert isinstance(proyecto.created_at, datetime)
        assert isinstance(proyecto.updated_at, datetime)

        # Verificar que persiste en BD
        session.refresh(proyecto)
        assert proyecto.id is not None

    def test_crear_proyecto_sin_descripcion(self, service):
        """Verifica crear un proyecto válido sin descripción (default vacío)."""
        data = ProyectoCreate(nombre="Solo Nombre")
        proyecto = service.crear(data)

        assert proyecto.id is not None
        assert proyecto.nombre == "Solo Nombre"
        assert proyecto.descripcion == ""
        assert proyecto.activo is True


class TestListarProyectos:
    """Tests para la operación listar del servicio."""

    def test_listar_solo_activos(self, service, session):
        """Verifica que listar_activos retorna solo proyectos con activo=True."""
        # Crear proyectos activos
        p1 = Proyecto(nombre="Activo 1")
        p2 = Proyecto(nombre="Activo 2")
        # Crear proyecto archivado
        p3 = Proyecto(nombre="Archivado", activo=False)
        session.add_all([p1, p2, p3])
        session.commit()

        activos = service.listar_activos()

        assert len(activos) == 2
        nombres = {p.nombre for p in activos}
        assert "Activo 1" in nombres
        assert "Activo 2" in nombres
        assert "Archivado" not in nombres

    def test_listar_orden_descendente_por_created_at(self, service, session):
        """Verifica que los proyectos se listan ordenados por created_at DESC."""
        import time

        p1 = Proyecto(nombre="Primero")
        session.add(p1)
        session.commit()
        time.sleep(0.01)

        p2 = Proyecto(nombre="Segundo")
        session.add(p2)
        session.commit()
        time.sleep(0.01)

        p3 = Proyecto(nombre="Tercero")
        session.add(p3)
        session.commit()

        activos = service.listar_activos()

        assert len(activos) == 3
        # El último creado debe ser el primero en la lista
        assert activos[0].nombre == "Tercero"
        assert activos[1].nombre == "Segundo"
        assert activos[2].nombre == "Primero"

    def test_lista_vacia_cuando_no_hay_proyectos(self, service):
        """Verifica que retorna lista vacía cuando no hay proyectos."""
        activos = service.listar_activos()
        assert activos == []


class TestObtenerProyecto:
    """Tests para la operación obtener del servicio."""

    def test_obtener_por_id_existente(self, service, session):
        """Verifica obtener un proyecto existente por ID."""
        proyecto = Proyecto(nombre="Encontrarme")
        session.add(proyecto)
        session.commit()

        resultado = service.obtener_por_id(proyecto.id)
        assert resultado is not None
        assert resultado.id == proyecto.id
        assert resultado.nombre == "Encontrarme"

    def test_obtener_por_id_inexistente_retorna_none(self, service):
        """Verifica que obtener un ID inexistente retorna None."""
        resultado = service.obtener_por_id(999)
        assert resultado is None


class TestActualizarProyecto:
    """Tests para la operación actualizar del servicio."""

    def test_actualizar_nombre_proyecto_existente(self, service, session):
        """Verifica actualizar el nombre de un proyecto existente."""
        proyecto = Proyecto(nombre="Original")
        session.add(proyecto)
        session.commit()

        data = ProyectoUpdate(nombre="Actualizado")
        resultado = service.actualizar(proyecto.id, data)

        assert resultado is not None
        assert resultado.nombre == "Actualizado"
        # La descripción no debe cambiar
        assert resultado.descripcion == ""

    def test_actualizar_solo_descripcion(self, service, session):
        """Verifica actualizar solo la descripción de un proyecto."""
        proyecto = Proyecto(nombre="Test", descripcion="Vieja desc")
        session.add(proyecto)
        session.commit()

        data = ProyectoUpdate(descripcion="Nueva descripción")
        resultado = service.actualizar(proyecto.id, data)

        assert resultado is not None
        assert resultado.descripcion == "Nueva descripción"
        # El nombre no debe cambiar
        assert resultado.nombre == "Test"

    def test_actualizar_proyecto_inexistente_retorna_none(self, service):
        """Verifica que actualizar un ID inexistente retorna None."""
        data = ProyectoUpdate(nombre="Nuevo")
        resultado = service.actualizar(999, data)
        assert resultado is None

    def test_actualizar_actualiza_updated_at(self, service, session):
        """Verifica que updated_at se actualiza al modificar el proyecto."""
        proyecto = Proyecto(nombre="Antes")
        session.add(proyecto)
        session.commit()

        updated_at_original = proyecto.updated_at

        # Esperar un momento para que el timestamp sea diferente
        import time

        time.sleep(0.01)

        data = ProyectoUpdate(nombre="Después")
        resultado = service.actualizar(proyecto.id, data)

        assert resultado is not None
        assert resultado.updated_at > updated_at_original


class TestArchivarProyecto:
    """Tests para la operación archivar del servicio."""

    def test_archivar_proyecto_cambia_activo_a_false(self, service, session):
        """Verifica que archivar proyecto establece activo=False."""
        proyecto = Proyecto(nombre="Para Archivar")
        session.add(proyecto)
        session.commit()
        assert proyecto.activo is True

        resultado = service.archivar(proyecto.id)

        assert resultado is not None
        assert resultado.activo is False

    def test_archivar_actualiza_updated_at(self, service, session):
        """Verifica que archivar actualiza updated_at."""
        import time

        proyecto = Proyecto(nombre="Temporal")
        session.add(proyecto)
        session.commit()
        updated_at_original = proyecto.updated_at

        time.sleep(0.01)

        resultado = service.archivar(proyecto.id)

        assert resultado is not None
        assert resultado.updated_at > updated_at_original

    def test_archivar_proyecto_inexistente_retorna_none(self, service):
        """Verifica que archivar un ID inexistente retorna None."""
        resultado = service.archivar(999)
        assert resultado is None
