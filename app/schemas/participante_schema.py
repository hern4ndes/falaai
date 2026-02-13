from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ParticipanteBase(BaseModel):
    nome:str
    telefone:str
    is_active:bool

class ParticipanteCreate(ParticipanteBase): 
    perfil:str

class ParticipanteUpdate(BaseModel):
    nome:Optional[str] = None
    telefone:Optional[str] = None
    perfil:Optional[str] = None
    is_active:Optional[bool]=None

class ParticipantePublic(ParticipanteBase):
    id:int
    data_cadastro:datetime
    perfil: str

    class Config:
        from_attributes=True



