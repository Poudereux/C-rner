"""Punto de entrada FastAPI.

Aplica SRP: este módulo solo monta la aplicación, conecta routers y
gestiona excepciones globales.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.logging_config import logger
from .database.session import crear_tablas, session_scope
from .domain.exceptions import BibliotecaError
from .repositories.libro_repository import LibroRepository
from .repositories.usuario_repository import UsuarioRepository
from .routers import libros, prestamos, usuarios

app = FastAPI(
    title=settings.app_name,
    description="API REST para gestionar el catálogo y préstamos de una biblioteca.",
    version="2.0.0",
)

app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)


@app.exception_handler(BibliotecaError)
async def biblioteca_error_handler(_: Request, exc: BibliotecaError) -> JSONResponse:
    """Mapea excepciones de dominio a respuestas HTTP coherentes."""
    logger.warning("BibliotecaError %s: %s", type(exc).__name__, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": str(exc)},
    )


@app.on_event("startup")
def on_startup() -> None:
    crear_tablas()
    if settings.seed_on_startup:
        _seed_inicial()


def _seed_inicial() -> None:
    """Inserta datos de ejemplo si la BD está vacía (para no salir 'pelado')."""
    with session_scope() as db:
        libros_repo = LibroRepository(db)
        usuarios_repo = UsuarioRepository(db)
        if libros_repo.listar():
            return
        ejemplos = [
            ("The Great Gatsby", "F. Scott Fitzgerald", "Clásico"),
            ("1984", "George Orwell", "Distopía"),
            ("Python Crash Course", "Eric Matthes", "Técnico"),
            ("Clean Code", "Robert C. Martin", "Técnico"),
            ("The Pragmatic Programmer", "Andrew Hunt", "Técnico"),
        ]
        for titulo, autor, genero in ejemplos:
            libros_repo.crear(titulo=titulo, autor=autor, genero=genero)
        if not usuarios_repo.listar():
            usuarios_repo.crear(nombre="Ada Lovelace", email="ada@biblioteca.es")
            usuarios_repo.crear(nombre="Alan Turing", email="alan@biblioteca.es")
        logger.info("Datos de ejemplo insertados.")


@app.get("/", tags=["meta"])
def root() -> dict:
    return {"app": settings.app_name, "version": app.version, "docs": "/docs"}
