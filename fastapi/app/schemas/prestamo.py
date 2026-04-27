"""Esquemas Pydantic para préstamos."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    cerrado: bool
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class PrestamoHistorial(BaseModel):
    """Préstamo con datos enriquecidos para mostrar en el historial."""

    id: int
    libro_id: int
    libro_titulo: str
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    activo: bool
