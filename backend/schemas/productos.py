from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    codigo: str | None = Field(default=None, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    precio_costo: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    precio_venta: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    cantidad: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    proveedor_id: int = Field(gt=0)
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    codigo: str | None = Field(default=None, max_length=50)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    precio_costo: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    precio_venta: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    cantidad: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    proveedor_id: int | None = Field(default=None, gt=0)
    activo: bool | None = None


class ProductoResponse(ProductoBase):
    id: int
    fecha_carga: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    