"""Tests para la configuración de la aplicación."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from core.config import Settings, settings


class TestSettingsFromEnv:
    """Tests que verifican que Settings lea correctamente las variables de entorno.

    Los valores de entorno son inyectados por ``tests/conftest.py``.
    """

    def test_settings_reads_app_name_from_env(self):
        """Lee APP_NAME desde variable de entorno."""
        s = Settings()
        assert s.app_name == "TaskRegistry"

    def test_settings_reads_app_version_from_env(self):
        """Lee APP_VERSION desde variable de entorno."""
        s = Settings()
        assert s.app_version == "0.1.0"

    def test_settings_reads_debug_from_env(self):
        """Lee DEBUG desde variable de entorno y lo convierte a bool."""
        s = Settings()
        assert s.debug is True

    def test_settings_reads_log_level_from_env(self):
        """Lee LOG_LEVEL desde variable de entorno."""
        s = Settings()
        assert s.log_level == "DEBUG"

    def test_settings_reads_database_url_from_env(self):
        """Lee DATABASE_URL desde variable de entorno."""
        s = Settings()
        assert s.database_url.startswith("sqlite:///")

    def test_settings_reads_data_dirs_from_env(self):
        """Lee DATA_DIR y DOCS_DIR desde variables de entorno."""
        s = Settings()
        assert s.data_dir == Path("data")
        assert s.docs_dir == Path("data/docs")

    def test_settings_azure_fields_default_to_empty(self):
        """Los campos de Azure DevOps deben ser string vacío por defecto."""
        s = Settings()
        assert s.azure_devops_org == ""
        assert s.azure_devops_project == ""
        assert s.azure_devops_pat == ""


class TestSettingsRequiredFields:
    """Tests que verifican que los campos obligatorios fallen si faltan.

    Para probar esto, deshabilitamos la carga del archivo ``.env`` y
    removemos temporalmente la variable de entorno correspondiente.
    """

    def test_settings_raises_without_app_name(self, monkeypatch):
        """Sin APP_NAME debe lanzar ValidationError."""
        monkeypatch.delenv("APP_NAME", raising=False)
        with pytest.raises(ValidationError, match="app_name"):
            Settings(_env_file=None)  # type: ignore[call-arg]

    def test_settings_raises_without_database_url(self, monkeypatch):
        """Sin DATABASE_URL debe lanzar ValidationError."""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        with pytest.raises(ValidationError, match="database_url"):
            Settings(_env_file=None)  # type: ignore[call-arg]

    def test_settings_raises_without_debug(self, monkeypatch):
        """Sin DEBUG debe lanzar ValidationError."""
        monkeypatch.delenv("DEBUG", raising=False)
        with pytest.raises(ValidationError, match="debug"):
            Settings(_env_file=None)  # type: ignore[call-arg]

    def test_settings_raises_without_log_level(self, monkeypatch):
        """Sin LOG_LEVEL debe lanzar ValidationError."""
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        with pytest.raises(ValidationError, match="log_level"):
            Settings(_env_file=None)  # type: ignore[call-arg]


class TestSettingsSingleton:
    """Tests para la instancia singleton ``settings``."""

    def test_singleton_settings_is_instance(self):
        """``settings`` debe ser una instancia de Settings."""
        assert isinstance(settings, Settings)

    def test_singleton_settings_has_required_fields(self):
        """La instancia singleton debe tener todos los campos requeridos."""
        assert settings.app_name
        assert settings.app_version
        assert settings.debug is not None
        assert settings.log_level
        assert settings.database_url
        assert settings.data_dir
        assert settings.docs_dir
