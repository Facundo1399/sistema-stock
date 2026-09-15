from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from config import Base


class Productos(Base):
    __tablename__ = "productos"

    id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
    codigo = Column(String(50), unique=True)
    nombre = Column(String(100), nullable=False, index= True)
    precio_costo = Column(Numeric(10, 2), nullable=False, default=0.00)
    precio_venta = Column(Numeric(10, 2), nullable=False, default=0.00)
    cantidad = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    # NOT NULL: todo producto debe tener proveedor.
    # En la DB la FK es ON DELETE RESTRICT: no se puede borrar un
    # proveedor mientras tenga productos asociados.
    proveedor_id = Column(
        MYSQL_INTEGER(unsigned=True),
        ForeignKey("proveedores.id", ondelete="RESTRICT"),
        nullable=False,
    )
    activo = Column(Boolean, nullable=False, default=True, server_default="1")
    fecha_carga = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
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