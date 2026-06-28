"""Tests para la configuración de logging."""

import logging

from core.logging_config import setup_logging


class TestLoggingConfig:
    """Tests para setup_logging."""

    def test_setup_logging_configures_root_logger(self):
        """Verifica que setup_logging configure el logger raíz."""
        # Resetear handlers para el test
        root = logging.getLogger()
        old_handlers = list(root.handlers)
        root.handlers.clear()

        try:
            setup_logging()
            assert len(root.handlers) > 0
            assert any(isinstance(h, logging.StreamHandler) for h in root.handlers)
        finally:
            # Restaurar handlers originales
            root.handlers.clear()
            for h in old_handlers:
                root.addHandler(h)
