from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RolUsuario(str, Enum):
    ADMIN = "admin"
    VENDEDOR = "vendedor"


class UserBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    rol: RolUsuario = RolUsuario.VENDEDOR
    activo: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)


class UserUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=255)
    rol: RolUsuario | None = None
    activo: bool | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
