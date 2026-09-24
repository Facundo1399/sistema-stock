from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from schemas.detalles import VentaDetalleCreate, VentaDetalleResponse


class VentaCreate(BaseModel):
	usuario_id: int | None = Field(default=None, gt=0)
	metodo_pago: Literal["efectivo", "transferencia", "tarjeta"] = "efectivo"
	detalles: list[VentaDetalleCreate] = Field(min_length=1)


class VentaResponse(BaseModel):
	id: int
	fecha: datetime
	usuario_id: int | None
	total: Decimal
	metodo_pago: Literal["efectivo", "transferencia", "tarjeta"]
	anulado: bool
	created_at: datetime
	detalles: list[VentaDetalleResponse]

	model_config = ConfigDict(from_attributes=True)
