"""Cliente HTTP que envuelve las llamadas a la API FastAPI.

Centraliza la URL y la gestion de errores para que las paginas no
repitan codigo (DRY) y para no acoplar Streamlit a la implementacion
concreta del backend (DIP en sentido amplio).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

# Si Streamlit corre en Docker apunta al servicio fastapi; en local, a
# localhost. La variable API_URL puede sobreescribirlo.
API_URL = os.getenv("API_URL", "http://localhost:8000")


class ApiError(Exception):
    """Error devuelto por la API."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")


def _check(response: requests.Response) -> Any:
    if response.ok:
        return response.json() if response.content else None
    try:
        body = response.json()
        detail = body.get("detail") or body.get("error") or response.text
        if isinstance(detail, list):
            detail = "; ".join(str(d.get("msg", d)) for d in detail)
    except ValueError:
        detail = response.text
    raise ApiError(response.status_code, str(detail))


# ---------------------------------------------------------------------------
# LIBROS
# ---------------------------------------------------------------------------
@st.cache_data(ttl=15)
def listar_libros(q: Optional[str] = None) -> List[Dict[str, Any]]:
    """Cacheado 10s para no machacar a la API en cada interaccion."""
    params = {"q": q} if q else {}
    r = requests.get(f"{API_URL}/libros/", params=params, timeout=5)
    return _check(r)


def crear_libro(titulo: str, autor: str, genero: str) -> Dict[str, Any]:
    r = requests.post(
        f"{API_URL}/libros/",
        json={"titulo": titulo, "autor": autor, "genero": genero},
        timeout=5,
    )
    resultado = _check(r)
    listar_libros.clear()  # invalida la cache
    return resultado


# ---------------------------------------------------------------------------
# USUARIOS
# ---------------------------------------------------------------------------
@st.cache_data(ttl=15)
def listar_usuarios() -> List[Dict[str, Any]]:
    r = requests.get(f"{API_URL}/usuarios/", timeout=5)
    return _check(r)


def crear_usuario(nombre: str, email: str) -> Dict[str, Any]:
    r = requests.post(
        f"{API_URL}/usuarios/",
        json={"nombre": nombre, "email": email},
        timeout=5,
    )
    resultado = _check(r)
    listar_usuarios.clear()
    return resultado


# ---------------------------------------------------------------------------
# PRESTAMOS
# ---------------------------------------------------------------------------
def crear_prestamo(libro_id: int, usuario_id: int) -> Dict[str, Any]:
    r = requests.post(
        f"{API_URL}/prestamos/",
        json={"libro_id": libro_id, "usuario_id": usuario_id},
        timeout=5,
    )
    resultado = _check(r)
    listar_libros.clear()
    return resultado


def devolver_prestamo(prestamo_id: int) -> Dict[str, Any]:
    r = requests.post(
        f"{API_URL}/prestamos/{prestamo_id}/devolver", timeout=5
    )
    resultado = _check(r)
    listar_libros.clear()
    return resultado


def historial_usuario(usuario_id: int) -> List[Dict[str, Any]]:
    r = requests.get(
        f"{API_URL}/prestamos/usuario/{usuario_id}/historial", timeout=5
    )
    return _check(r)
