from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioAdminBase(BaseModel):
    email: EmailStr
    nome: str


class UsuarioAdminCreate(UsuarioAdminBase):
    senha: str


class UsuarioAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    senha: Optional[str] = None


class UsuarioAdminPublic(UsuarioAdminBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None
