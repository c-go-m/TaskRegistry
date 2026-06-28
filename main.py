"""Punto de entrada de la aplicación TaskRegistry."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.database import create_db_and_tables
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Manejador de ciclo de vida de la aplicación.

    Args:
        _app: Instancia de FastAPI.

    Yields:
        None: la aplicación se ejecuta mientras el contexto está activo.
    """
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI.

    Returns:
        Instancia de FastAPI configurada.
    """
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Bitácora personal de tareas laborales",
        lifespan=lifespan,
    )

    static_dir = Path("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    def root():
        return RedirectResponse(url="/docs")

    return app


app = create_app()
