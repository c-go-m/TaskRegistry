"""Tests para la configuración de la aplicación."""

from pathlib import Path

from core.config import Settings, settings


class TestSettings:
    """Tests para la clase Settings."""

    def test_settings_has_default_values(self):
        """Verifica que Settings tenga valores por defecto."""
        s = Settings()
        assert s.app_name == "TaskRegistry"
        assert s.app_version == "0.1.0"
        assert s.debug is True
        assert s.log_level == "DEBUG"

    def test_settings_has_database_url(self):
        """Verifica que Settings tenga DATABASE_URL."""
        s = Settings()
        assert s.database_url.startswith("sqlite:///")

    def test_settings_has_azure_fields(self):
        """Verifica que Settings tenga campos para Azure DevOps."""
        s = Settings()
        assert hasattr(s, "azure_devops_org")
        assert hasattr(s, "azure_devops_project")
        assert hasattr(s, "azure_devops_pat")

    def test_settings_has_data_dirs(self):
        """Verifica que Settings tenga rutas de datos."""
        s = Settings()
        assert s.data_dir == Path("data")
        assert s.docs_dir == Path("data/docs")

    def test_singleton_settings_exists(self):
        """Verifica que exista una instancia singleton 'settings'."""
        assert settings is not None
        assert isinstance(settings, Settings)
