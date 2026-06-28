"""Script para ejecutar la aplicación en desarrollo."""

import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
    )
