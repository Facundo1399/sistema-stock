from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, String, func
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from config import Base


class RolUsuario(str, PyEnum):
    ADMIN = "admin"
    VENDEDOR = "vendedor"


class User(Base):
    __tablename__ = "users"

    id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    rol = Column(
        Enum(RolUsuario, name="rol"),
        nullable=False,
        default=RolUsuario.VENDEDOR,
        server_default="vendedor",
    )
    activo = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )