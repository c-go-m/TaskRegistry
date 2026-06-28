"""Fábricas de dependencias para FastAPI."""

import logging
from collections.abc import Generator

from sqlmodel import Session

from core.database import get_session

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """Dependencia que provee una sesión de base de datos.

    Yields:
        Sesión de SQLModel lista para usar.
    """
    yield from get_session()


def get_logger() -> logging.Logger:
    """Dependencia que provee un logger configurado.

    Returns:
        Logger del módulo core.dependencies.
    """
    return logger
