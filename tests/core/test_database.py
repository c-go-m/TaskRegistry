"""Tests para la configuración de base de datos."""

from unittest.mock import patch

import pytest
from sqlmodel import SQLModel

from core.database import create_db_and_tables, engine, get_engine, get_session


class TestDatabase:
    """Tests para las funciones de base de datos."""

    def test_get_engine_returns_engine(self):
        """Verifica que get_engine retorne un engine."""
        eng = get_engine()
        assert eng is not None
        assert str(eng.url).startswith("sqlite:///")

    def test_engine_singleton_exists(self):
        """Verifica que exista engine como singleton."""
        assert engine is not None

    def test_create_db_and_tables_runs(self):
        """Verifica que create_db_and_tables ejecute sin errores."""
        with patch.object(SQLModel.metadata, "create_all") as mock_create:
            create_db_and_tables()
            mock_create.assert_called_once_with(engine)

    def test_get_session_yields_session(self):
        """Verifica que get_session sea un generador que retorna una sesión."""
        gen = get_session()
        session = next(gen)
        assert session is not None
        # Cerrar la sesión
        with pytest.raises(StopIteration):
            next(gen)
