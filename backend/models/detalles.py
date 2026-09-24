from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from sqlalchemy.orm import relationship

from config import Base


class VentasDetalles(Base):
	__tablename__ = "ventas_detalles"

	id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
	venta_id = Column(
		MYSQL_INTEGER(unsigned=True),
		ForeignKey("ventas.id", ondelete="CASCADE"),
		nullable=False,
	)
	producto_id = Column(
		MYSQL_INTEGER(unsigned=True),
		ForeignKey("productos.id"),
		nullable=False,
	)
	cantidad = Column(Integer, nullable=False)
	precio_unitario = Column(Numeric(10, 2), nullable=False)
	subtotal = Column(Numeric(10, 2), nullable=False)

	venta = relationship("Ventas", back_populates="detalles")
	producto = relationship("Productos")
