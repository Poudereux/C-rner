"""Servicio de usuarios (HU-03)."""
from __future__ import annotations

from typing import List

from ..core.decorators import log_call
from ..domain.exceptions import (
    DatosInvalidosError,
    EmailDuplicadoError,
    UsuarioNoEncontradoError,
)
from ..domain.models import Usuario
from ..repositories.base import UsuarioRepositoryProtocol


class UsuarioService:
    def __init__(self, repo: UsuarioRepositoryProtocol) -> None:
        self._repo = repo

    @log_call
    def listar(self) -> List[Usuario]:
        return self._repo.listar()

    @log_call
    def obtener(self, usuario_id: int) -> Usuario:
        usuario = self._repo.obtener(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(
                f"No existe ningún usuario con id {usuario_id}."
            )
        return usuario

    @log_call
    def crear(self, nombre: str, email: str) -> Usuario:
        """HU-03: registra un nuevo usuario."""
        if not nombre.strip() or not email.strip():
            raise DatosInvalidosError("Nombre y email son obligatorios.")

        if self._repo.por_email(email.strip()) is not None:
            raise EmailDuplicadoError(
                f"Ya existe un usuario con el email {email}."
            )

        return self._repo.crear(nombre=nombre.strip(), email=email.strip())
