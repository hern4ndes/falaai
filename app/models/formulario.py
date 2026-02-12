from datetime import datetime

from sqlalchemy import String, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class Formulario(Base):
    __tablename__ = "formularios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    formulario_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ativo",
        server_default="ativo",
    )

    data_criacao: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        server_default=text("NOW()"),
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        server_default=text("NOW()"),
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('ativo', 'inativo', 'rascunho')",
            name="check_formulario_status_valido",
        ),
    )

    def __repr__(self) -> str:
        return f"<Formulario(id={self.id}, status='{self.status}')>"
