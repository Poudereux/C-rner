"""Tests unitarios del LibroService usando mocks (Aprobado)."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import DatosInvalidosError, LibroNoEncontradoError
from app.domain.models import Libro
from app.services.libro_service import LibroService


def _libro(id_=1, titulo="1984", autor="George Orwell", genero="Distopía"):
    return Libro(id=id_, titulo=titulo, autor=autor, genero=genero)


def test_listar_devuelve_lo_que_da_el_repo():
    repo = MagicMock()
    repo.listar.return_value = [_libro()]
    service = LibroService(repo)

    resultado = service.listar()

    assert len(resultado) == 1
    assert resultado[0].titulo == "1984"
    repo.listar.assert_called_once()


def test_crear_lanza_si_falta_titulo():
    service = LibroService(MagicMock())
    with pytest.raises(DatosInvalidosError):
        service.crear(titulo="  ", autor="Autor", genero="Género")


def test_crear_lanza_si_falta_autor():
    service = LibroService(MagicMock())
    with pytest.raises(DatosInvalidosError):
        service.crear(titulo="Titulo", autor="", genero="Género")


def test_crear_normaliza_y_llama_al_repo():
    repo = MagicMock()
    repo.crear.return_value = _libro()
    service = LibroService(repo)

    service.crear("  El Quijote  ", " Cervantes ", " Clásico ")

    repo.crear.assert_called_once_with(
        titulo="El Quijote", autor="Cervantes", genero="Clásico"
    )


def test_obtener_lanza_si_no_existe():
    repo = MagicMock()
    repo.obtener.return_value = None
    service = LibroService(repo)

    with pytest.raises(LibroNoEncontradoError):
        service.obtener(99)


def test_buscar_vacio_devuelve_listar():
    repo = MagicMock()
    repo.listar.return_value = [_libro()]
    service = LibroService(repo)

    service.buscar("   ")

    repo.listar.assert_called_once()
    repo.buscar.assert_not_called()


def test_buscar_con_texto_pasa_al_repo():
    repo = MagicMock()
    repo.buscar.return_value = []
    service = LibroService(repo)

    service.buscar("Orwell")

    repo.buscar.assert_called_once_with("Orwell")


def test_buscar_solo_whitespace_devuelve_listar():
    """Caso limite: tabs y saltos de linea cuentan como busqueda vacia."""
    repo = MagicMock()
    repo.listar.return_value = []
    service = LibroService(repo)

    service.buscar("\t\n  ")

    repo.listar.assert_called_once()
    repo.buscar.assert_not_called()
