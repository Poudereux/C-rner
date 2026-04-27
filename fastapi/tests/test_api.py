"""Tests de integración con TestClient.

Cubren el ciclo completo: crear libro → crear usuario → prestar →
devolver → consultar historial. Usan SQLite en memoria.
"""
from __future__ import annotations


def test_flujo_completo(client):
    # HU-02: registrar libro
    r = client.post(
        "/libros/",
        json={"titulo": "1984", "autor": "George Orwell", "genero": "Distopía"},
    )
    assert r.status_code == 201, r.text
    libro_id = r.json()["id"]

    # HU-01: catálogo
    r = client.get("/libros/")
    assert r.status_code == 200
    assert any(l["titulo"] == "1984" for l in r.json())

    # HU-07: búsqueda case-insensitive parcial
    r = client.get("/libros/?q=orwell")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # HU-03: registrar usuario
    r = client.post("/usuarios/", json={"nombre": "Ada", "email": "ada@b.es"})
    assert r.status_code == 201, r.text
    usuario_id = r.json()["id"]

    # HU-03: email duplicado debe fallar con 409
    r = client.post("/usuarios/", json={"nombre": "Otra", "email": "ada@b.es"})
    assert r.status_code == 409

    # HU-04: prestar
    r = client.post(
        "/prestamos/", json={"libro_id": libro_id, "usuario_id": usuario_id}
    )
    assert r.status_code == 201, r.text
    prestamo_id = r.json()["id"]

    # Tras el préstamo, el libro está no disponible
    r = client.get(f"/libros/{libro_id}")
    assert r.json()["disponible"] is False

    # No se puede prestar dos veces
    r = client.post(
        "/prestamos/", json={"libro_id": libro_id, "usuario_id": usuario_id}
    )
    assert r.status_code == 409

    # HU-05: devolver
    r = client.post(f"/prestamos/{prestamo_id}/devolver")
    assert r.status_code == 200
    r = client.get(f"/libros/{libro_id}")
    assert r.json()["disponible"] is True

    # No se puede devolver dos veces
    r = client.post(f"/prestamos/{prestamo_id}/devolver")
    assert r.status_code == 409

    # HU-06: historial
    r = client.get(f"/prestamos/usuario/{usuario_id}/historial")
    assert r.status_code == 200
    historial = r.json()
    assert len(historial) == 1
    assert historial[0]["activo"] is False


def test_libro_invalido_devuelve_422(client):
    # Pydantic valida campos vacíos vía Field(min_length=1)
    r = client.post(
        "/libros/", json={"titulo": "", "autor": "A", "genero": "G"}
    )
    assert r.status_code == 422


def test_libro_inexistente_devuelve_404(client):
    r = client.get("/libros/9999")
    assert r.status_code == 404


def test_prestar_libro_inexistente_devuelve_404(client):
    r = client.post("/prestamos/", json={"libro_id": 999, "usuario_id": 999})
    assert r.status_code == 404


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "version" in r.json()
