"""Sesión de base de datos y context manager para usarla con `with`.

Usar `session_scope()` con `with` (criterio Sobresaliente: context managers)
garantiza que la sesión siempre se cierra, haciendo commit si todo va bien
o rollback si hay excepción.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..core.config import settings
from ..core.logging_config import logger
from ..domain.models import Base

# `connect_args` es necesario para SQLite cuando se usa multi-thread
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def crear_tablas() -> None:
    """Crea todas las tablas declaradas en `Base.metadata`."""
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas (si no existían).")


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provee una sesión transaccional dentro de un bloque `with`.

    Hace commit al salir limpiamente y rollback si se levanta excepción.
    """
    sesion = SessionLocal()
    try:
        yield sesion
        sesion.commit()
    except Exception:
        sesion.rollback()
        raise
    finally:
        sesion.close()


def get_db() -> Iterator[Session]:
    """Dependencia de FastAPI: provee una sesión por request."""
    sesion = SessionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
