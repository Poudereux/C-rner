"""Endpoints de usuarios (HU-03)."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..schemas.usuario import UsuarioCreate, UsuarioOut
from ..services.usuario_service import UsuarioService
from .dependencies import get_usuario_service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(
    service: UsuarioService = Depends(get_usuario_service),
) -> List[UsuarioOut]:
    return [UsuarioOut.model_validate(u) for u in service.listar()]


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    payload: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service),
    db: Session = Depends(get_db),
) -> UsuarioOut:
    usuario = service.crear(payload.nombre, str(payload.email))
    db.commit()
    db.refresh(usuario)
    return UsuarioOut.model_validate(usuario)


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service),
) -> UsuarioOut:
    return UsuarioOut.model_validate(service.obtener(usuario_id))
