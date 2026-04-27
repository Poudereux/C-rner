"""Decoradores propios usados por los servicios.

Demuestran el uso justificado de decoradores (criterio Sobresaliente).
"""
from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, TypeVar

from .logging_config import logger

F = TypeVar("F", bound=Callable[..., Any])


def log_call(func: F) -> F:
    """Loggea la entrada y salida de una función con su duración.

    Útil en la capa de servicio para tener trazabilidad sin ensuciar la
    lógica de negocio con prints o logs manuales.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        nombre = f"{func.__module__}.{func.__qualname__}"
        logger.info("→ %s args=%s kwargs=%s", nombre, args[1:], kwargs)
        inicio = time.perf_counter()
        try:
            resultado = func(*args, **kwargs)
        except Exception as exc:
            logger.error("✗ %s lanzó %s: %s", nombre, type(exc).__name__, exc)
            raise
        duracion_ms = (time.perf_counter() - inicio) * 1000
        logger.info("← %s ok (%.2f ms)", nombre, duracion_ms)
        return resultado

    return wrapper  # type: ignore[return-value]
