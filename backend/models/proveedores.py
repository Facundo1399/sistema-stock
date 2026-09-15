from sqlalchemy import Column, Boolean, Integer, String, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from config import Base


class Proveedore(Base):
    __tablename__ = "proveedores"

    id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(30), nullable=False)
    email = Column(String(100))
    direccion = Column(String(100))
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