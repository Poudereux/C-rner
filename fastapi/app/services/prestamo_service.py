"""Servicio de préstamos (HU-04, HU-05, HU-06)."""
from __future__ import annotations

from typing import List

from ..core.decorators import log_call
from ..domain.exceptions import (
    LibroNoDisponibleError,
    LibroNoEncontradoError,
    PrestamoNoEncontradoError,
    PrestamoYaCerradoError,
    UsuarioNoEncontradoError,
)
from ..domain.models import Prestamo
from ..repositories.base import (
    LibroRepositoryProtocol,
    PrestamoRepositoryProtocol,
    UsuarioRepositoryProtocol,
)


class PrestamoService:
    def __init__(
        self,
        prestamo_repo: PrestamoRepositoryProtocol,
        libro_repo: LibroRepositoryProtocol,
        usuario_repo: UsuarioRepositoryProtocol,
    ) -> None:
        self._prestamos = prestamo_repo
        self._libros = libro_repo
        self._usuarios = usuario_repo

    @log_call
    def crear(self, libro_id: int, usuario_id: int) -> Prestamo:
        """HU-04: presta un libro a un usuario."""
        libro = self._libros.obtener(libro_id)
        if libro is None:
            raise LibroNoEncontradoError(f"No existe el libro con id {libro_id}.")

        usuario = self._usuarios.obtener(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(
                f"No existe el usuario con id {usuario_id}."
            )

        if not libro.disponible:
            raise LibroNoDisponibleError(
                f"El libro '{libro.titulo}' ya está prestado."
            )

        return self._prestamos.crear(libro_id=libro_id, usuario_id=usuario_id)

    @log_call
    def devolver(self, prestamo_id: int) -> Prestamo:
        """HU-05: cierra un préstamo activo."""
        prestamo = self._prestamos.obtener(prestamo_id)
        if prestamo is None:
            raise PrestamoNoEncontradoError(
                f"No existe el préstamo con id {prestamo_id}."
            )
        if prestamo.cerrado:
            raise PrestamoYaCerradoError(
                f"El préstamo {prestamo_id} ya estaba cerrado."
            )
        prestamo.cerrar()
        return prestamo

    @log_call
    def historial_usuario(self, usuario_id: int) -> List[Prestamo]:
        """HU-06: historial completo de un usuario (activos y cerrados)."""
        if self._usuarios.obtener(usuario_id) is None:
            raise UsuarioNoEncontradoError(
                f"No existe el usuario con id {usuario_id}."
            )
        return self._prestamos.por_usuario(usuario_id)
