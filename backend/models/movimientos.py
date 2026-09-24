from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from config import Base


class MovimientosStock(Base):
    __tablename__ = "movimientos_stock"

    id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
    producto_id = Column(
        MYSQL_INTEGER(unsigned=True),
        ForeignKey("productos.id"),
        nullable=False,
    )
    tipo = Column(
        Enum("entrada", "salida", "ajuste", name="tipo_movimiento"),
        nullable=False,
    )
    cantidad = Column(Integer, nullable=False)
    cantidad_anterior = Column(Integer, nullable=False)
    cantidad_nueva = Column(Integer, nullable=False)
    motivo = Column(String(100))
    usuario_id = Column(
        MYSQL_INTEGER(unsigned=True),
        ForeignKey("users.id"),
    )
    referencia_id = Column(MYSQL_INTEGER(unsigned=True))
    fecha = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )