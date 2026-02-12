from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.formulario import Formulario


class FormularioCRUD:
    async def get(self, session: AsyncSession, formulario_id: int) -> Optional[Formulario]:
        return await session.get(Formulario, formulario_id)

    async def list(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Iterable[Formulario]:
        stmt = select(Formulario).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        *,
        formulario_json: dict,
        status: str = "ativo",
    ) -> Formulario:
        formulario = Formulario(formulario_json=formulario_json, status=status)
        session.add(formulario)
        await session.commit()
        await session.refresh(formulario)
        return formulario

    async def update(
        self,
        session: AsyncSession,
        formulario: Formulario,
        *,
        formulario_json: Optional[dict] = None,
        status: Optional[str] = None,
    ) -> Formulario:
        if formulario_json is not None:
            formulario.formulario_json = formulario_json
        if status is not None:
            formulario.status = status

        await session.commit()
        await session.refresh(formulario)
        return formulario

    async def remove(self, session: AsyncSession, formulario: Formulario) -> None:
        await session.delete(formulario)
        await session.commit()


formulario_crud = FormularioCRUD()
