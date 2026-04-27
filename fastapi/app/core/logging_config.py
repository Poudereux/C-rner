"""Configuración del logger de la aplicación.

Tres niveles de logging (INFO, WARNING, ERROR) tal y como exige el enunciado.
"""
from __future__ import annotations

import logging
import sys

from .config import settings


def setup_logging() -> logging.Logger:
    """Configura y devuelve el logger raíz de la aplicación."""
    logger = logging.getLogger("biblioteca")

    # Evita duplicar handlers si setup_logging se llama dos veces
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logging()
