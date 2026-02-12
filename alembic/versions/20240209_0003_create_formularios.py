"""create formularios table

Revision ID: 20240209_0003
Revises: 20240209_0002
Create Date: 2026-02-12

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = "20240209_0003"
down_revision = "20240209_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "formularios",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column("formulario_json", JSONB(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ativo"),
        sa.Column("data_criacao", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("data_atualizacao", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.CheckConstraint(
            "status IN ('ativo', 'inativo', 'rascunho')",
            name="check_formulario_status_valido",
        ),
    )
    op.create_index("ix_formularios_id", "formularios", ["id"])


def downgrade() -> None:
    op.drop_index("ix_formularios_id", table_name="formularios")
    op.drop_table("formularios")
