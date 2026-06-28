"""Configuración de logging centralizada."""

import logging
import sys

from core.config import settings


def setup_logging():
    """Configura el logging para la aplicación.

    Establece un formato estructurado con timestamp, nivel, módulo y mensaje.
    El output se envía a stdout y a un archivo taskregistry.log en data/.
    """
    log_format = "%(asctime)s | %(levelname)-8s | " "%(name)s:%(funcName)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.DEBUG),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    log_dir = settings.data_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(
        log_dir / "taskregistry.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logging.getLogger().addHandler(file_handler)
