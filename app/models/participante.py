from sqlalchemy import String,Boolean
from sqlalchemy.orm import mapped_column,Mapped
from app.db.base import Base
from datetime import datetime
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func

class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False) 
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default = func.now(),
        nullable=False)
    perfil:Mapped[str] = mapped_column(String(255), nullable=False) 
    is_active: Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
  



