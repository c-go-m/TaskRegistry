"""Tests para las dependencias de FastAPI."""

import logging

from core.dependencies import get_db, get_logger


class TestDependencies:
    """Tests para las fábricas de dependencias."""

    def test_get_db_returns_generator(self):
        """Verifica que get_db sea un generador."""
        gen = get_db()
        assert hasattr(gen, "__next__")
        assert hasattr(gen, "__iter__")

    def test_get_logger_returns_logger(self):
        """Verifica que get_logger retorne un logger."""
        logger = get_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == "core.dependencies"
