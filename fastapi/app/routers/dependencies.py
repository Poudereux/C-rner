"""Dependency injection helpers para los routers.

Aplica DIP: los routers reciben servicios ya cableados.
"""
from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..repositories.libro_repository import LibroRepository
from ..repositories.prestamo_repository import PrestamoRepository
from ..repositories.usuario_repository import UsuarioRepository
from ..services.libro_service import LibroService
from ..services.prestamo_service import PrestamoService
from ..services.usuario_service import UsuarioService


def get_libro_service(db: Session = Depends(get_db)) -> LibroService:
    return LibroService(LibroRepository(db))


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


def get_prestamo_service(db: Session = Depends(get_db)) -> PrestamoService:
    return PrestamoService(
        prestamo_repo=PrestamoRepository(db),
        libro_repo=LibroRepository(db),
        usuario_repo=UsuarioRepository(db),
    )
