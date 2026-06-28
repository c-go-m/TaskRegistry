"""Configuración global de tests para TaskRegistry.

Establece variables de entorno necesarias para que ``Settings()`` pueda
instanciarse sin depender del archivo ``.env``.

Las variables se definen con ``setdefault``, por lo que si ya existen en
el entorno (p. ej. en CI) respetan el valor externo.
"""

import os


def pytest_configure(config) -> None:
    """Configura variables de entorno antes de importar los módulos bajo test.

    Esta función es ejecutada por pytest antes de la recolección de tests,
    garantizando que ``core.config`` pueda instanciar ``Settings()`` sin
    valores por defecto.

    Args:
        config: Objeto de configuración de pytest (no usado directamente).
    """
    os.environ.setdefault("APP_NAME", "TaskRegistry")
    os.environ.setdefault("APP_VERSION", "0.1.0")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")
    os.environ.setdefault("DATABASE_URL", "sqlite:///data/test_taskregistry.db")
    os.environ.setdefault("DATA_DIR", "data")
    os.environ.setdefault("DOCS_DIR", "data/docs")
