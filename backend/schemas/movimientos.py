from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MovimientoCreate(BaseModel):
    """Lo único que decide el cliente."""
    producto_id: int = Field(gt=0)
    tipo: Literal["entrada", "salida", "ajuste"]
    cantidad: int
    motivo: str | None = Field(default=None, max_length=100)
    referencia_id: int | None = Field(default=None, gt=0)
    # SIN cantidad_anterior, cantidad_nueva, usuario_id, fecha:
    # el servidor los calcula/asigna, nunca vienen del cliente


class MovimientoResponse(BaseModel):
    """Sí expone todo — el cliente necesita ver el resultado."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    tipo: Literal["entrada", "salida", "ajuste"]
    cantidad: int
    cantidad_anterior: int
    cantidad_nueva: int
    motivo: str | None
    usuario_id: int | None
    referencia_id: int | None
    fecha: datetime