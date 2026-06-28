"""Configuración de la base de datos."""

from pathlib import Path

from sqlmodel import Session as DBSession
from sqlmodel import SQLModel, create_engine

from core.config import settings


def get_engine():
    """Crea y retorna el engine de SQLAlchemy.

    Returns:
        Engine configurado de SQLAlchemy/SQLModel.
    """
    db_path = Path(settings.database_url.replace("sqlite:///", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
    return engine


engine = get_engine()


def create_db_and_tables():
    """Crea todas las tablas definidas en los modelos SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Generador de sesiones de base de datos (para dependencias FastAPI).

    Yields:
        Session de SQLModel.
    """
    with DBSession(engine) as session:
        yield session
