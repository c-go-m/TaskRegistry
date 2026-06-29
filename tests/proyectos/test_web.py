"""Tests para las vistas web (Jinja2 + HTMX) del módulo de proyectos.

RED phase: estos tests deben fallar inicialmente porque los endpoints web
aún son placeholders y no existen los templates.
"""

from pathlib import Path
from tempfile import mkdtemp

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from proyectos.modelos import Proyecto

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def db_path():
    """Crea un path temporal para la base de datos SQLite de pruebas web."""
    tmp_dir = Path(mkdtemp())
    return tmp_dir / "test_proyectos_web.db"


@pytest.fixture
def engine(db_path):
    """Crea un engine SQLite con archivo temporal."""
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def override_get_db(engine):
    """Factory para sobrescribir get_db con sesión de prueba."""

    def _get_db():
        with Session(engine) as session:
            yield session

    return _get_db


@pytest.fixture
def client(override_get_db):
    """Crea un cliente de prueba con el router web y dependencias sobrescritas."""
    from core.dependencies import get_db
    from proyectos.router import router_web

    app = FastAPI()
    app.include_router(router_web)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    """Crea una sesión directa para setup de datos en tests."""
    with Session(engine) as s:
        yield s


# ---------------------------------------------------------------------------
# Tests — Listado web
# ---------------------------------------------------------------------------


class TestListarProyectosWeb:
    """Tests para GET /proyectos/."""

    def test_retorna_html(self, client):
        """Verifica que GET /proyectos/ retorna content-type text/html."""
        response = client.get("/proyectos/")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")

    def test_sin_proyectos_muestra_empty_state(self, client):
        """Verifica que sin proyectos se muestra mensaje de lista vacía."""
        response = client.get("/proyectos/")
        assert response.status_code == 200
        assert "No hay proyectos activos" in response.text

    def test_con_proyectos_muestra_tabla(self, client, session):
        """Verifica que con proyectos se renderiza la tabla."""
        session.add_all([
            Proyecto(nombre="Proyecto Alpha", descripcion="Descripción Alpha"),
            Proyecto(nombre="Proyecto Beta"),
        ])
        session.commit()

        response = client.get("/proyectos/")
        assert response.status_code == 200
        assert "Proyecto Alpha" in response.text
        assert "Proyecto Beta" in response.text
        assert "Descripción Alpha" in response.text

    def test_excluye_proyectos_archivados(self, client, session):
        """Verifica que proyectos archivados no aparecen en la tabla."""
        session.add_all([
            Proyecto(nombre="Activo"),
            Proyecto(nombre="Archivado", activo=False),
        ])
        session.commit()

        response = client.get("/proyectos/")
        assert response.status_code == 200
        assert "Activo" in response.text
        assert "Archivado" not in response.text


# ---------------------------------------------------------------------------
# Tests — Formulario de creación
# ---------------------------------------------------------------------------


class TestFormularioCrear:
    """Tests para GET /proyectos/nuevo."""

    def test_muestra_formulario_con_texto_crear(self, client):
        """Verifica que el formulario contiene el texto 'Crear'."""
        response = client.get("/proyectos/nuevo")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        assert "Crear" in response.text

    def test_formulario_tiene_campo_nombre(self, client):
        """Verifica que el formulario tiene un campo para el nombre."""
        response = client.get("/proyectos/nuevo")
        assert 'name="nombre"' in response.text or "nombre" in response.text.lower()


# ---------------------------------------------------------------------------
# Tests — Formulario de edición
# ---------------------------------------------------------------------------


class TestFormularioEditar:
    """Tests para GET /proyectos/{proyecto_id}/editar."""

    def test_muestra_formulario_precargado(self, client, session):
        """Verifica que el formulario de edición muestra datos precargados."""
        proyecto = Proyecto(nombre="Proyecto Editable", descripcion="Descripción editable")
        session.add(proyecto)
        session.commit()

        response = client.get(f"/proyectos/{proyecto.id}/editar")
        assert response.status_code == 200
        assert "Actualizar" in response.text
        assert "Proyecto Editable" in response.text

    def test_proyecto_inexistente_retorna_404(self, client):
        """Verifica que editar un ID inexistente retorna 404."""
        response = client.get("/proyectos/999/editar")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests — Acciones HTMX
# ---------------------------------------------------------------------------


class TestCrearProyectoWeb:
    """Tests para POST /proyectos/ (HTMX)."""

    def test_crear_proyecto_desde_formulario(self, client):
        """Verifica que crear vía POST redirige o actualiza la tabla."""
        response = client.post(
            "/proyectos/",
            data={"nombre": "Nuevo Web", "descripcion": "Creado desde HTMX"},
        )
        # Debe redirigir a la lista o retornar el partial de tabla
        assert response.status_code in (200, 302, 303)

    def test_crear_proyecto_sin_nombre_retorna_error(self, client):
        """Verifica que crear sin nombre retorna error."""
        response = client.post(
            "/proyectos/",
            data={"nombre": "", "descripcion": "Sin nombre"},
        )
        assert response.status_code == 422


class TestArchivarProyectoWeb:
    """Tests para PATCH /proyectos/{proyecto_id}/archivar (HTMX)."""

    def test_archivar_proyecto_existente(self, client, session):
        """Verifica que archivar un proyecto vía HTMX retorna éxito."""
        proyecto = Proyecto(nombre="Para Archivar Web")
        session.add(proyecto)
        session.commit()

        response = client.patch(f"/proyectos/{proyecto.id}/archivar")
        # Debe retornar el partial de tabla actualizado
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")

    def test_archivar_proyecto_inexistente_retorna_404(self, client):
        """Verifica que archivar un ID inexistente retorna 404."""
        response = client.patch("/proyectos/999/archivar")
        assert response.status_code == 404
