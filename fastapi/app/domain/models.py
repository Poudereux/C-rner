"""Modelos SQLAlchemy 2.x del dominio.

Sustituyen al CSV original. Cada entidad encapsula su responsabilidad
(SRP) y expone propiedades calculadas con @property (criterio
Sobresaliente).
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Clase base de SQLAlchemy 2.x para todos los modelos."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower() + "s"


class Libro(Base):
    """Libro del catálogo."""

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    autor: Mapped[str] = mapped_column(String(200), nullable=False)
    genero: Mapped[str] = mapped_column(String(100), nullable=False)

    prestamos: Mapped[List["Prestamo"]] = relationship(
        back_populates="libro",
        cascade="all, delete-orphan",
    )

    @property
    def disponible(self) -> bool:
        """Un libro está disponible si no tiene préstamos activos."""
        return not any(p.activo for p in self.prestamos)

    def __repr__(self) -> str:
        return f"<Libro id={self.id} titulo={self.titulo!r}>"


class Usuario(Base):
    """Usuario registrado de la biblioteca."""

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)

    prestamos: Mapped[List["Prestamo"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("email", name="uq_usuario_email"),)

    @property
    def prestamos_activos(self) -> List["Prestamo"]:
        return [p for p in self.prestamos if p.activo]

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email!r}>"


class Prestamo(Base):
    """Préstamo de un libro a un usuario."""

    id: Mapped[int] = mapped_column(primary_key=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False
    )
    fecha_prestamo: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    fecha_devolucion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    cerrado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    libro: Mapped["Libro"] = relationship(back_populates="prestamos")
    usuario: Mapped["Usuario"] = relationship(back_populates="prestamos")

    @property
    def activo(self) -> bool:
        """Un préstamo es activo mientras no se haya cerrado."""
        return not self.cerrado

    def cerrar(self, ahora: Optional[datetime] = None) -> None:
        """Marca el préstamo como devuelto."""
        self.cerrado = True
        self.fecha_devolucion = ahora or datetime.utcnow()

    def __repr__(self) -> str:
        return (
            f"<Prestamo id={self.id} libro_id={self.libro_id} "
            f"usuario_id={self.usuario_id} activo={self.activo}>"
        )
