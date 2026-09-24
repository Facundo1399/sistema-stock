from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Numeric, func
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from sqlalchemy.orm import relationship

from config import Base


class Ventas(Base):
	__tablename__ = "ventas"

	id = Column(MYSQL_INTEGER(unsigned=True), primary_key=True, index=True)
	fecha = Column(
		DateTime,
		nullable=False,
		server_default=func.current_timestamp(),
	)
	usuario_id = Column(MYSQL_INTEGER(unsigned=True), ForeignKey("users.id"))
	total = Column(Numeric(10, 2), nullable=False, default=0.00)
	metodo_pago = Column(
		Enum("efectivo", "transferencia", "tarjeta", name="metodo_pago"),
		nullable=False,
		server_default="efectivo",
	)
	anulado = Column(Boolean, nullable=False, default=False, server_default="0")
	created_at = Column(
		DateTime,
		nullable=False,
		server_default=func.current_timestamp(),
	)

	detalles = relationship(
		"VentasDetalles",
		back_populates="venta",
		cascade="all, delete-orphan",
	)
