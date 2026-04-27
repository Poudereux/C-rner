"""Tests unitarios del PrestamoService."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import (
    LibroNoDisponibleError,
    LibroNoEncontradoError,
    PrestamoNoEncontradoError,
    PrestamoYaCerradoError,
    UsuarioNoEncontradoError,
)
from app.domain.models import Libro, Prestamo, Usuario
from app.services.prestamo_service import PrestamoService


def _service(libro=None, usuario=None, prestamo=None):
    libro_repo = MagicMock()
    usuario_repo = MagicMock()
    prestamo_repo = MagicMock()
    libro_repo.obtener.return_value = libro
    usuario_repo.obtener.return_value = usuario
    prestamo_repo.obtener.return_value = prestamo
    prestamo_repo.crear.return_value = Prestamo(id=10, libro_id=1, usuario_id=1)
    return (
        PrestamoService(prestamo_repo, libro_repo, usuario_repo),
        libro_repo,
        usuario_repo,
        prestamo_repo,
    )


def test_crear_lanza_si_libro_no_existe():
    service, *_ = _service(libro=None, usuario=Usuario(id=1, nombre="A", email="a@a"))
    with pytest.raises(LibroNoEncontradoError):
        service.crear(1, 1)


def test_crear_lanza_si_usuario_no_existe():
    service, *_ = _service(
        libro=Libro(id=1, titulo="t", autor="a", genero="g"), usuario=None
    )
    with pytest.raises(UsuarioNoEncontradoError):
        service.crear(1, 1)


def test_crear_lanza_si_libro_no_disponible():
    libro = Libro(id=1, titulo="t", autor="a", genero="g")
    libro.prestamos = [Prestamo(id=99, libro_id=1, usuario_id=1, cerrado=False)]
    service, *_ = _service(libro=libro, usuario=Usuario(id=1, nombre="A", email="a@a"))
    with pytest.raises(LibroNoDisponibleError):
        service.crear(1, 1)


def test_crear_ok_llama_al_repo():
    libro = Libro(id=1, titulo="t", autor="a", genero="g")
    libro.prestamos = []
    service, _, _, prestamo_repo = _service(
        libro=libro, usuario=Usuario(id=1, nombre="A", email="a@a")
    )
    service.crear(1, 1)
    prestamo_repo.crear.assert_called_once_with(libro_id=1, usuario_id=1)


def test_devolver_lanza_si_no_existe():
    service, *_ = _service(prestamo=None)
    with pytest.raises(PrestamoNoEncontradoError):
        service.devolver(1)


def test_devolver_lanza_si_ya_cerrado():
    p = Prestamo(id=1, libro_id=1, usuario_id=1, cerrado=True)
    service, *_ = _service(prestamo=p)
    with pytest.raises(PrestamoYaCerradoError):
        service.devolver(1)


def test_devolver_marca_cerrado():
    p = Prestamo(id=1, libro_id=1, usuario_id=1, cerrado=False)
    service, *_ = _service(prestamo=p)
    service.devolver(1)
    assert p.cerrado is True
    assert p.fecha_devolucion is not None


def test_historial_lanza_si_usuario_no_existe():
    service, *_ = _service(usuario=None)
    with pytest.raises(UsuarioNoEncontradoError):
        service.historial_usuario(99)


def test_historial_devuelve_lo_que_da_el_repo():
    p1 = Prestamo(id=1, libro_id=1, usuario_id=1, cerrado=False)
    p2 = Prestamo(id=2, libro_id=2, usuario_id=1, cerrado=True)
    service, _, _, prestamo_repo = _service(
        usuario=Usuario(id=1, nombre="A", email="a@a")
    )
    prestamo_repo.por_usuario.return_value = [p1, p2]
    historial = service.historial_usuario(1)
    assert len(historial) == 2
