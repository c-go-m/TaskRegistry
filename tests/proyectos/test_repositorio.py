"""Tests para el repositorio de Proyecto.

RED phase: estos tests deben fallar inicialmente porque repositorio.py
aún no existe.
"""


import pytest
from sqlmodel import Session, SQLModel, create_engine

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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAdd:
    """Tests para ProyectoRepository.add."""

    def test_add_asigna_id(self, repo, session):
        """Verifica que add asigna un ID al proyecto."""
        proyecto = Proyecto(nombre="Nuevo")
        resultado = repo.add(proyecto)

        assert resultado.id is not None
        assert resultado.nombre == "Nuevo"
        # Verificar que está en BD
        session.refresh(proyecto)
        assert proyecto.id is not None

    def test_add_persiste_en_bd(self, repo, session):
        """Verifica que add persiste el proyecto en base de datos."""
        proyecto = Proyecto(nombre="Persistente", descripcion="Test")
        repo.add(proyecto)

        # Recuperar de BD directamente
        desde_bd = session.get(Proyecto, proyecto.id)
        assert desde_bd is not None
        assert desde_bd.nombre == "Persistente"
        assert desde_bd.descripcion == "Test"


class TestGet:
    """Tests para ProyectoRepository.get."""

    def test_get_por_id_existente(self, repo, session):
        """Verifica que get retorna un proyecto existente."""
        proyecto = Proyecto(nombre="Buscado")
        session.add(proyecto)
        session.commit()

        resultado = repo.get(proyecto.id)
        assert resultado is not None
        assert resultado.nombre == "Buscado"

    def test_get_por_id_inexistente_retorna_none(self, repo):
        """Verifica que get retorna None para ID inexistente."""
        resultado = repo.get(999)
        assert resultado is None

    def test_get_incluye_proyectos_archivados(self, repo, session):
        """Verifica que get también retorna proyectos archivados."""
        proyecto = Proyecto(nombre="Archivado", activo=False)
        session.add(proyecto)
        session.commit()

        resultado = repo.get(proyecto.id)
        assert resultado is not None
        assert resultado.activo is False


class TestListActivos:
    """Tests para ProyectoRepository.list_activos."""

    def test_lista_solo_activos(self, repo, session):
        """Verifica que list_activos retorna solo proyectos con activo=True."""
        p1 = Proyecto(nombre="Activo 1")
        p2 = Proyecto(nombre="Activo 2")
        p3 = Proyecto(nombre="Archivado", activo=False)
        session.add_all([p1, p2, p3])
        session.commit()

        activos = repo.list_activos()

        assert len(activos) == 2
        nombres = {p.nombre for p in activos}
        assert "Activo 1" in nombres
        assert "Activo 2" in nombres
        assert "Archivado" not in nombres

    def test_lista_orden_descendente_por_created_at(self, repo, session):
        """Verifica orden descendente por created_at."""
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

        activos = repo.list_activos()

        assert len(activos) == 3
        assert activos[0].nombre == "Tercero"
        assert activos[1].nombre == "Segundo"
        assert activos[2].nombre == "Primero"

    def test_lista_vacia_sin_proyectos(self, repo):
        """Verifica que retorna lista vacía cuando no hay proyectos."""
        assert repo.list_activos() == []


class TestSave:
    """Tests para ProyectoRepository.save."""

    def test_save_persiste_cambios(self, repo, session):
        """Verifica que save persiste cambios en un proyecto existente."""
        proyecto = Proyecto(nombre="Original")
        session.add(proyecto)
        session.commit()

        proyecto.nombre = "Modificado"
        proyecto.descripcion = "Nueva desc"
        resultado = repo.save(proyecto)

        assert resultado.nombre == "Modificado"
        assert resultado.descripcion == "Nueva desc"

        # Verificar en BD
        session.refresh(proyecto)
        assert proyecto.nombre == "Modificado"

    def test_save_actualiza_updated_at(self, repo, session):
        """Verifica que save actualiza el timestamp updated_at."""
        import time

        proyecto = Proyecto(nombre="Temporal")
        session.add(proyecto)
        session.commit()
        updated_at_original = proyecto.updated_at

        time.sleep(0.01)
        proyecto.nombre = "Cambiado"
        resultado = repo.save(proyecto)

        assert resultado.updated_at > updated_at_original
