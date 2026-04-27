"""Fixtures de pytest.

Cada test que necesite BD recibe una sesion SQLAlchemy con SQLite en
memoria - aislada del resto de tests y rapidisima.
"""
from __future__ import annotations

import os
from typing import Iterator

# Forzamos BD en memoria ANTES de importar nada de la app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SEED_ON_STARTUP"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import get_db
from app.domain.models import Base
from app.main import app


@pytest.fixture()
def engine():
    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    try:
        yield eng
    finally:
        Base.metadata.drop_all(eng)
        eng.dispose()


@pytest.fixture()
def db(engine) -> Iterator[Session]:
    SessionTesting = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    sesion = SessionTesting()
    try:
        yield sesion
    finally:
        sesion.close()


@pytest.fixture()
def client(engine) -> Iterator[TestClient]:
    SessionTesting = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def _override_get_db() -> Iterator[Session]:
        sesion = SessionTesting()
        try:
            yield sesion
        finally:
            sesion.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
