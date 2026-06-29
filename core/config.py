"""
Configuración de la aplicación usando pydantic-settings.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Ruta absoluta al archivo .env en la raíz del proyecto
# (se resuelve desde la ubicación de este archivo, no desde el CWD)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Configuración de la aplicación.

    Lee variables de entorno desde el archivo ``.env`` en la raíz del proyecto.
    Todas las variables —excepto las de Azure DevOps— son obligatorias.
    """

    # Metadatos
    app_name: str
    app_version: str
    debug: bool
    log_level: str

    # Base de datos
    database_url: str

    # Azure DevOps (opcional — por defecto string vacío)
    azure_devops_org: str = ""
    azure_devops_project: str = ""
    azure_devops_pat: str = ""

    # Rutas
    data_dir: Path
    docs_dir: Path

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
