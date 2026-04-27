"""Repositorio de libros sobre SQLAlchemy."""
from __future__ import annotations

from typing import Iterable, List, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..domain.models import Libro


class LibroRepository:
    """Acceso a datos para Libro (SRP)."""

    def __init__(self, sesion: Session) -> None:
        self._s = sesion

    def listar(self) -> List[Libro]:
        return list(self._s.scalars(select(Libro).order_by(Libro.id)).all())

    def obtener(self, libro_id: int) -> Optional[Libro]:
        return self._s.get(Libro, libro_id)

    def crear(self, titulo: str, autor: str, genero: str) -> Libro:
        libro = Libro(titulo=titulo, autor=autor, genero=genero)
        self._s.add(libro)
        self._s.flush()  # asigna el id sin cerrar la transacción
        return libro

    def buscar(self, texto: str) -> List[Libro]:
        """Busca por título o autor (case-insensitive, parcial)."""
        patron = f"%{texto.lower()}%"
        stmt = select(Libro).where(
            or_(
                Libro.titulo.ilike(patron),
                Libro.autor.ilike(patron),
            )
        ).order_by(Libro.id)
        return list(self._s.scalars(stmt).all())

    def stream(self) -> Iterable[Libro]:
        """Generador (yield) sobre todos los libros.

        Útil para procesar grandes catálogos sin cargarlos enteros en
        memoria (criterio Sobresaliente: generadores).
        """
        for libro in self._s.scalars(select(Libro).order_by(Libro.id)).yield_per(100):
            yield libro
