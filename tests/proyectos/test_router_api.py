"""Tests para los endpoints REST API del módulo de proyectos.

RED phase: estos tests deben fallar inicialmente porque router.py
aún no existe.
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
    """Crea un path temporal para la base de datos SQLite."""
    tmp_dir = Path(mkdtemp())
    return tmp_dir / "test_proyectos.db"


@pytest.fixture
def engine(db_path):
    """Crea un engine SQLite con archivo temporal para soportar múltiples hilos."""
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    # Limpiar después de los tests
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def override_get_db(engine):
    """Factory para sobrescribir la dependencia get_db con una sesión de prueba."""

    def _get_db():
        with Session(engine) as session:
            yield session

    return _get_db


@pytest.fixture
def client(override_get_db):
    """Crea un cliente de prueba con el router API y dependencias sobrescritas."""
    from core.dependencies import get_db
    from proyectos.router import router_api

    app = FastAPI()
    app.include_router(router_api)
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
# Tests
# ---------------------------------------------------------------------------


class TestCrearProyecto:
    """Tests para POST /api/proyectos/."""

    def test_crear_proyecto_retorna_201(self, client):
        """Verifica que crear un proyecto retorna status 201."""
        response = client.post(
            "/api/proyectos/",
            json={"nombre": "Nuevo Proyecto"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Nuevo Proyecto"
        assert data["descripcion"] == ""
        assert data["activo"] is True
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_crear_proyecto_con_descripcion(self, client):
        """Verifica crear un proyecto con descripción."""
        response = client.post(
            "/api/proyectos/",
            json={"nombre": "Con Desc", "descripcion": "Una descripción"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Con Desc"
        assert data["descripcion"] == "Una descripción"

    def test_crear_proyecto_sin_nombre_retorna_422(self, client):
        """Verifica que crear sin nombre retorna 422."""
        response = client.post(
            "/api/proyectos/",
            json={"nombre": ""},
        )
        assert response.status_code == 422

    def test_crear_proyecto_sin_body_retorna_422(self, client):
        """Verifica que crear sin body retorna 422."""
        response = client.post("/api/proyectos/", json={})
        assert response.status_code == 422


class TestListarProyectos:
    """Tests para GET /api/proyectos/."""

    def test_listar_con_proyectos(self, client, session):
        """Verifica que listar retorna los proyectos creados."""
        # Crear datos de prueba directamente
        session.add_all([
            Proyecto(nombre="Proyecto A"),
            Proyecto(nombre="Proyecto B"),
        ])
        session.commit()

        response = client.get("/api/proyectos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        nombres = {p["nombre"] for p in data}
        assert "Proyecto A" in nombres
        assert "Proyecto B" in nombres

    def test_listar_excluye_archivados(self, client, session):
        """Verifica que listar excluye proyectos archivados."""
        session.add_all([
            Proyecto(nombre="Activo"),
            Proyecto(nombre="Archivado", activo=False),
        ])
        session.commit()

        response = client.get("/api/proyectos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Activo"

    def test_listar_sin_proyectos_retorna_lista_vacia(self, client):
        """Verifica que listar sin proyectos retorna lista vacía."""
        response = client.get("/api/proyectos/")
        assert response.status_code == 200
        assert response.json() == []


class TestObtenerProyecto:
    """Tests para GET /api/proyectos/{proyecto_id}."""

    def test_obtener_existente_retorna_200(self, client, session):
        """Verifica que obtener un proyecto existente retorna 200."""
        proyecto = Proyecto(nombre="Detalle")
        session.add(proyecto)
        session.commit()

        response = client.get(f"/api/proyectos/{proyecto.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == proyecto.id
        assert data["nombre"] == "Detalle"

    def test_obtener_inexistente_retorna_404(self, client):
        """Verifica que obtener un ID inexistente retorna 404."""
        response = client.get("/api/proyectos/999")
        assert response.status_code == 404
        assert "detail" in response.json()


class TestActualizarProyecto:
    """Tests para PUT /api/proyectos/{proyecto_id}."""

    def test_actualizar_existente_retorna_200(self, client, session):
        """Verifica actualizar un proyecto existente."""
        proyecto = Proyecto(nombre="Original")
        session.add(proyecto)
        session.commit()

        response = client.put(
            f"/api/proyectos/{proyecto.id}",
            json={"nombre": "Actualizado", "descripcion": "Nueva desc"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Actualizado"
        assert data["descripcion"] == "Nueva desc"

    def test_actualizar_solo_nombre(self, client, session):
        """Verifica actualizar solo el nombre."""
        proyecto = Proyecto(nombre="Original", descripcion="Desc original")
        session.add(proyecto)
        session.commit()

        response = client.put(
            f"/api/proyectos/{proyecto.id}",
            json={"nombre": "SoloNombre"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "SoloNombre"
        # La descripción no debe cambiar
        assert data["descripcion"] == "Desc original"

    def test_actualizar_inexistente_retorna_404(self, client):
        """Verifica que actualizar un ID inexistente retorna 404."""
        response = client.put(
            "/api/proyectos/999",
            json={"nombre": "Nuevo"},
        )
        assert response.status_code == 404


class TestArchivarProyecto:
    """Tests para PATCH /api/proyectos/{proyecto_id}/archivar."""

    def test_archivar_existente_retorna_200_con_activo_false(self, client, session):
        """Verifica archivar un proyecto existente."""
        proyecto = Proyecto(nombre="Para Archivar")
        session.add(proyecto)
        session.commit()

        response = client.patch(f"/api/proyectos/{proyecto.id}/archivar")
        assert response.status_code == 200
        data = response.json()
        assert data["activo"] is False

    def test_archivar_inexistente_retorna_404(self, client):
        """Verifica que archivar un ID inexistente retorna 404."""
        response = client.patch("/api/proyectos/999/archivar")
        assert response.status_code == 404
