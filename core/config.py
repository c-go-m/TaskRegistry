"""Configuración de la aplicación usando pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación.

    Lee variables de entorno desde el archivo .env en la raíz del proyecto.
    """

    # Metadatos
    app_name: str = "TaskRegistry"
    app_version: str = "0.1.0"
    debug: bool = True
    log_level: str = "DEBUG"

    # Base de datos
    database_url: str = "sqlite:///data/taskregistry.db"

    # Azure DevOps
    azure_devops_org: str = ""
    azure_devops_project: str = ""
    azure_devops_pat: str = ""

    # Rutas
    data_dir: Path = Path("data")
    docs_dir: Path = Path("data/docs")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
