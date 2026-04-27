"""Tests de los repositorios contra una BD SQLite en memoria."""
from __future__ import annotations

from app.repositories.libro_repository import LibroRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.usuario_repository import UsuarioRepository


def test_libro_crear_y_listar(db):
    repo = LibroRepository(db)
    repo.crear("1984", "George Orwell", "Distopía")
    repo.crear("It", "Stephen King", "Terror")
    db.commit()

    libros = repo.listar()
    assert len(libros) == 2
    assert {l.titulo for l in libros} == {"1984", "It"}


def test_libro_buscar_es_case_insensitive(db):
    repo = LibroRepository(db)
    repo.crear("1984", "George Orwell", "Distopía")
    repo.crear("It", "Stephen King", "Terror")
    db.commit()

    resultados = repo.buscar("orwell")
    assert len(resultados) == 1
    assert resultados[0].autor == "George Orwell"


def test_libro_stream_es_un_generador(db):
    repo = LibroRepository(db)
    repo.crear("Libro", "Autor", "Género")
    db.commit()
    gen = repo.stream()
    # stream() debe ser un generador, no una lista
    assert hasattr(gen, "__iter__")
    libros = list(gen)
    assert len(libros) == 1


def test_usuario_por_email(db):
    repo = UsuarioRepository(db)
    repo.crear("Ada", "ada@b.es")
    db.commit()
    assert repo.por_email("ada@b.es") is not None
    assert repo.por_email("nope@b.es") is None


def test_prestamo_activos_por_libro(db):
    libros = LibroRepository(db)
    usuarios = UsuarioRepository(db)
    prestamos = PrestamoRepository(db)
    libro = libros.crear("L", "A", "G")
    usuario = usuarios.crear("U", "u@u.es")
    prestamos.crear(libro.id, usuario.id)
    db.commit()

    activos = prestamos.activos_por_libro(libro.id)
    assert len(activos) == 1
