"""Repositorio de usuarios."""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain.models import Usuario


class UsuarioRepository:
    def __init__(self, sesion: Session) -> None:
        self._s = sesion

    def listar(self) -> List[Usuario]:
        return list(self._s.scalars(select(Usuario).order_by(Usuario.id)).all())

    def obtener(self, usuario_id: int) -> Optional[Usuario]:
        return self._s.get(Usuario, usuario_id)

    def por_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.email == email)
        return self._s.scalars(stmt).first()

    def crear(self, nombre: str, email: str) -> Usuario:
        usuario = Usuario(nombre=nombre, email=email)
        self._s.add(usuario)
        self._s.flush()
        return usuario
