from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FormularioCreate(BaseModel):
    formulario_json: dict
    status: str = "ativo"


class FormularioUpdate(BaseModel):
    formulario_json: Optional[dict] = None
    status: Optional[str] = None


class FormularioPublic(BaseModel):
    id: int
    formulario_json: dict
    status: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True
