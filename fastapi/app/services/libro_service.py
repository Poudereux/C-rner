"""Servicio de libros (HU-01, HU-02, HU-07).

Aplica DIP: depende de un protocolo, no de la implementación concreta.
"""
from __future__ import annotations

from typing import List

from ..core.decorators import log_call
from ..domain.exceptions import DatosInvalidosError, LibroNoEncontradoError
from ..domain.models import Libro
from ..repositories.base import LibroRepositoryProtocol


class LibroService:
    def __init__(self, repo: LibroRepositoryProtocol) -> None:
        self._repo = repo

    @log_call
    def listar(self) -> List[Libro]:
        """HU-01: devuelve todos los libros."""
        return self._repo.listar()

    @log_call
    def crear(self, titulo: str, autor: str, genero: str) -> Libro:
        """HU-02: registra un nuevo libro."""
        if not titulo.strip() or not autor.strip() or not genero.strip():
            raise DatosInvalidosError(
                "Título, autor y género son obligatorios y no pueden estar vacíos."
            )
        return self._repo.crear(
            titulo=titulo.strip(),
            autor=autor.strip(),
            genero=genero.strip(),
        )

    @log_call
    def obtener(self, libro_id: int) -> Libro:
        libro = self._repo.obtener(libro_id)
        if libro is None:
            raise LibroNoEncontradoError(f"No existe ningún libro con id {libro_id}.")
        return libro

    @log_call
    def buscar(self, texto: str) -> List[Libro]:
        """HU-07: busca por título o autor (parcial, case-insensitive)."""
        if not texto.strip():
            return self._repo.listar()
        return self._repo.buscar(texto.strip())
