"""Endpoints de libros (HU-01, HU-02, HU-07)."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..schemas.libro import LibroCreate, LibroOut
from ..services.libro_service import LibroService
from .dependencies import get_libro_service

router = APIRouter(prefix="/libros", tags=["libros"])


@router.get("/", response_model=List[LibroOut])
def listar_libros(
    q: Optional[str] = None,
    service: LibroService = Depends(get_libro_service),
    _db: Session = Depends(get_db),
) -> List[LibroOut]:
    """Lista todos los libros o filtra por título/autor con `?q=texto`."""
    libros = service.buscar(q) if q else service.listar()
    return [
        LibroOut(
            id=l.id,
            titulo=l.titulo,
            autor=l.autor,
            genero=l.genero,
            disponible=l.disponible,
        )
        for l in libros
    ]


@router.post("/", response_model=LibroOut, status_code=status.HTTP_201_CREATED)
def crear_libro(
    payload: LibroCreate,
    service: LibroService = Depends(get_libro_service),
    db: Session = Depends(get_db),
) -> LibroOut:
    libro = service.crear(payload.titulo, payload.autor, payload.genero)
    db.commit()
    db.refresh(libro)
    return LibroOut(
        id=libro.id,
        titulo=libro.titulo,
        autor=libro.autor,
        genero=libro.genero,
        disponible=libro.disponible,
    )


@router.get("/{libro_id}", response_model=LibroOut)
def obtener_libro(
    libro_id: int,
    service: LibroService = Depends(get_libro_service),
) -> LibroOut:
    libro = service.obtener(libro_id)
    return LibroOut(
        id=libro.id,
        titulo=libro.titulo,
        autor=libro.autor,
        genero=libro.genero,
        disponible=libro.disponible,
    )
