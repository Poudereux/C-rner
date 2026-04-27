"""Esquemas Pydantic para usuarios."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    email: EmailStr


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str

    model_config = ConfigDict(from_attributes=True)
