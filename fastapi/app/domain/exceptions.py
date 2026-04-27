"""Excepciones personalizadas de dominio.

Permiten distinguir errores de negocio de errores técnicos y mapearlos
a códigos HTTP en la capa de API.
"""
from __future__ import annotations


class BibliotecaError(Exception):
    """Excepción raíz del dominio biblioteca."""

    status_code: int = 400


class RecursoNoEncontradoError(BibliotecaError):
    """Se intentó acceder a un recurso que no existe."""

    status_code = 404


class LibroNoEncontradoError(RecursoNoEncontradoError):
    """No existe ningún libro con el id indicado."""


class UsuarioNoEncontradoError(RecursoNoEncontradoError):
    """No existe ningún usuario con el id indicado."""


class PrestamoNoEncontradoError(RecursoNoEncontradoError):
    """No existe ningún préstamo con el id indicado."""


class ConflictoDatosError(BibliotecaError):
    """Conflicto al guardar (p. ej. email duplicado)."""

    status_code = 409


class EmailDuplicadoError(ConflictoDatosError):
    """Ya existe un usuario con ese email."""


class LibroNoDisponibleError(ConflictoDatosError):
    """El libro ya está prestado."""


class PrestamoYaCerradoError(ConflictoDatosError):
    """Se intentó devolver un préstamo que ya estaba cerrado."""


class DatosInvalidosError(BibliotecaError):
    """Faltan campos obligatorios o son incorrectos."""

    status_code = 422
