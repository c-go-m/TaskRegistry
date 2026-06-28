"""Tests para el punto de entrada de la aplicación."""

from fastapi.testclient import TestClient

from main import app


class TestMainApp:
    """Tests para la aplicación FastAPI."""

    def test_app_created(self):
        """Verifica que la app se haya creado correctamente."""
        assert app.title == "TaskRegistry"
        assert app.version == "0.1.0"

    def test_root_redirects_to_docs(self):
        """Verifica que la raíz redirija a /docs."""
        client = TestClient(app)
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"

    def test_docs_swagger_ui(self):
        """Verifica que Swagger UI esté accesible."""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_openapi_schema(self):
        """Verifica que el esquema OpenAPI esté disponible."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "TaskRegistry"
        assert data["info"]["version"] == "0.1.0"
