"""Repositorio de préstamos."""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain.models import Prestamo


class PrestamoRepository:
    def __init__(self, sesion: Session) -> None:
        self._s = sesion

    def crear(self, libro_id: int, usuario_id: int) -> Prestamo:
        prestamo = Prestamo(libro_id=libro_id, usuario_id=usuario_id)
        self._s.add(prestamo)
        self._s.flush()
        return prestamo

    def obtener(self, prestamo_id: int) -> Optional[Prestamo]:
        return self._s.get(Prestamo, prestamo_id)

    def activos_por_libro(self, libro_id: int) -> List[Prestamo]:
        stmt = select(Prestamo).where(
            Prestamo.libro_id == libro_id,
            Prestamo.cerrado.is_(False),
        )
        return list(self._s.scalars(stmt).all())

    def por_usuario(self, usuario_id: int) -> List[Prestamo]:
        stmt = (
            select(Prestamo)
            .where(Prestamo.usuario_id == usuario_id)
            .order_by(Prestamo.fecha_prestamo.desc())
        )
        return list(self._s.scalars(stmt).all())
