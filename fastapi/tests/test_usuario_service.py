"""Tests unitarios del UsuarioService."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import (
    DatosInvalidosError,
    EmailDuplicadoError,
    UsuarioNoEncontradoError,
)
from app.domain.models import Usuario
from app.services.usuario_service import UsuarioService


def test_crear_lanza_si_email_duplicado():
    repo = MagicMock()
    repo.por_email.return_value = Usuario(id=1, nombre="A", email="a@b.es")
    service = UsuarioService(repo)

    with pytest.raises(EmailDuplicadoError):
        service.crear("Otro", "a@b.es")


def test_crear_lanza_si_nombre_vacio():
    service = UsuarioService(MagicMock())
    with pytest.raises(DatosInvalidosError):
        service.crear("", "x@y.es")


def test_crear_lanza_si_email_vacio():
    service = UsuarioService(MagicMock())
    with pytest.raises(DatosInvalidosError):
        service.crear("Pepe", "")


def test_crear_ok_llama_al_repo():
    repo = MagicMock()
    repo.por_email.return_value = None
    repo.crear.return_value = Usuario(id=1, nombre="Pepe", email="p@e.es")
    service = UsuarioService(repo)

    usuario = service.crear("Pepe", "p@e.es")

    assert usuario.email == "p@e.es"
    repo.crear.assert_called_once()


def test_obtener_inexistente_lanza():
    repo = MagicMock()
    repo.obtener.return_value = None
    service = UsuarioService(repo)
    with pytest.raises(UsuarioNoEncontradoError):
        service.obtener(123)


def test_listar_delega_en_repo():
    repo = MagicMock()
    repo.listar.return_value = [Usuario(id=1, nombre="A", email="a@a.es")]
    service = UsuarioService(repo)
    assert len(service.listar()) == 1
