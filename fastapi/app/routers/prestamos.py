"""Endpoints de préstamos (HU-04, HU-05, HU-06)."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..schemas.prestamo import PrestamoCreate, PrestamoHistorial, PrestamoOut
from ..services.prestamo_service import PrestamoService
from .dependencies import get_prestamo_service

router = APIRouter(prefix="/prestamos", tags=["prestamos"])


@router.post("/", response_model=PrestamoOut, status_code=status.HTTP_201_CREATED)
def crear_prestamo(
    payload: PrestamoCreate,
    service: PrestamoService = Depends(get_prestamo_service),
    db: Session = Depends(get_db),
) -> PrestamoOut:
    prestamo = service.crear(payload.libro_id, payload.usuario_id)
    db.commit()
    db.refresh(prestamo)
    return PrestamoOut.model_validate(prestamo)


@router.post("/{prestamo_id}/devolver", response_model=PrestamoOut)
def devolver_prestamo(
    prestamo_id: int,
    service: PrestamoService = Depends(get_prestamo_service),
    db: Session = Depends(get_db),
) -> PrestamoOut:
    prestamo = service.devolver(prestamo_id)
    db.commit()
    db.refresh(prestamo)
    return PrestamoOut.model_validate(prestamo)


@router.get(
    "/usuario/{usuario_id}/historial",
    response_model=List[PrestamoHistorial],
)
def historial_usuario(
    usuario_id: int,
    service: PrestamoService = Depends(get_prestamo_service),
) -> List[PrestamoHistorial]:
    prestamos = service.historial_usuario(usuario_id)
    return [
        PrestamoHistorial(
            id=p.id,
            libro_id=p.libro_id,
            libro_titulo=p.libro.titulo if p.libro else "(libro borrado)",
            usuario_id=p.usuario_id,
            fecha_prestamo=p.fecha_prestamo,
            fecha_devolucion=p.fecha_devolucion,
            activo=p.activo,
        )
        for p in prestamos
    ]
