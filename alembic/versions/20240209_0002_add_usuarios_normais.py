"""add usuarios_normais table

Revision ID: 20240209_0002
Revises: 20240209_0001
Create Date: 2026-02-09

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240209_0002"
down_revision = "20240209_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usuarios_normais",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("funcao", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("email", name="uq_usuarios_normais_email"),
    )


def downgrade() -> None:
    op.drop_table("usuarios_normais")
