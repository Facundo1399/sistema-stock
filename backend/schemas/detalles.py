from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class VentaDetalleCreate(BaseModel):
	producto_id: int = Field(gt=0)
	cantidad: int = Field(gt=0)


class VentaDetalleResponse(BaseModel):
	id: int
	venta_id: int
	producto_id: int
	cantidad: int
	precio_unitario: Decimal
	subtotal: Decimal

	model_config = ConfigDict(from_attributes=True)
