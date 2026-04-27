"""Configuración central de la aplicación.

Aplica el principio SRP: una única razón para cambiar (la configuración).
Aplica DIP: el resto de la aplicación depende de esta abstracción, no de
literales hardcodeados.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Configuración inmutable cargada desde variables de entorno."""

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./biblioteca.db",
    )
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    app_name: str = os.getenv("APP_NAME", "Gestor de Bibliotecas")
    seed_on_startup: bool = os.getenv("SEED_ON_STARTUP", "true").lower() == "true"


settings = Settings()
