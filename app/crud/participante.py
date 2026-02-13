from app.models.participante import Participante
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, Optional
from sqlalchemy import select


class ParticipanteCRUD:
    async def create(self,session:AsyncSession, *, nome:str, telefone:str, perfil:str )->Participante:
        participante = Participante(nome=nome, telefone=telefone, perfil=perfil)
        session.add(participante)
        await session.commit()
        await session.refresh(participante)
        return participante

    async def update(self,session:AsyncSession,
     participante:Participante, 
     *, 
     nome:Optional[str]=None, 
     telefone:Optional[str]=None, 
     perfil:Optional[str]=None,
     is_active:Optional[bool]=None,
     )-> Participante:

        if nome is not None:
            participante.nome = nome
        if telefone is not None:
            participante.telefone = telefone
        if perfil is not None:
            participante.perfil = perfil
        if is_active is not None:
            participante.is_active = is_active
    
        await session.commit()
        await session.refresh(participante)
        return participante


    async def delete(self,session:AsyncSession, participante:Participante)->Participante:
        return await self.update(session,participante,is_active=False)
        #await session.delete(participante)
       #await session.commit()


    async def get(self,session:AsyncSession, participante_id: int)->Optional[Participante]:
        return await session.get(Participante, participante_id)
    

    async def get_by_telefone(self,session:AsyncSession, part_telefone:str)->Optional[Participante]:
        query = select(Participante).where(Participante.telefone == part_telefone)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    async def list(self,session:AsyncSession, *,skip: int =0, limit: int = 300) -> Iterable[Participante]:
        query = select(Participante).where(Participante.is_active==True).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


participante = ParticipanteCRUD()









