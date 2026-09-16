from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ProveedorBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    telefono: str = Field(min_length=1, max_length=30)
    email: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=100)
    activo: bool = True

class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    telefono: str | None = Field(default=None, min_length=1, max_length=30)
    email: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=100)
    activo: bool | None = None


class ProveedorResponse(ProveedorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)