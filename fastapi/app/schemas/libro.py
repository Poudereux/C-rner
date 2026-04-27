"""Esquemas Pydantic para libros."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LibroCreate(BaseModel):
    """Datos necesarios para crear un libro."""

    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=200)
    genero: str = Field(..., min_length=1, max_length=100)


class LibroOut(BaseModel):
    """Representación de un libro tal y como se devuelve al cliente."""

    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool

    model_config = ConfigDict(from_attributes=True)
