from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario_admin import UsuarioAdmin


class UsuarioAdminCRUD:
    async def get(self, session: AsyncSession, admin_id: int) -> Optional[UsuarioAdmin]:
        return await session.get(UsuarioAdmin, admin_id)

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UsuarioAdmin]:
        stmt = select(UsuarioAdmin).where(UsuarioAdmin.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> Iterable[UsuarioAdmin]:
        stmt = select(UsuarioAdmin).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        *,
        email: str,
        senha_hash: str,
        nome: str,
    ) -> UsuarioAdmin:
        admin = UsuarioAdmin(email=email, senha_hash=senha_hash, nome=nome)
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        return admin

    async def update(
        self,
        session: AsyncSession,
        admin: UsuarioAdmin,
        *,
        email: Optional[str] = None,
        senha_hash: Optional[str] = None,
        nome: Optional[str] = None,
    ) -> UsuarioAdmin:
        if email is not None:
            admin.email = email
        if senha_hash is not None:
            admin.senha_hash = senha_hash
        if nome is not None:
            admin.nome = nome

        await session.commit()
        await session.refresh(admin)
        return admin

    async def remove(self, session: AsyncSession, admin: UsuarioAdmin) -> None:
        await session.delete(admin)
        await session.commit()


usuario_admin = UsuarioAdminCRUD()
