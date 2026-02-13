from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.participante import participante
from app.db.session import get_db
from app.models.usuario_admin import UsuarioAdmin
from app.models.participante import Participante
from app.schemas.participante_schema import ParticipanteBase, ParticipanteCreate, ParticipantePublic, ParticipanteUpdate
from app.api.deps import get_current_admin

router = APIRouter(prefix="/participantes", tags=["participantes"])


@router.post("", response_model=ParticipantePublic, status_code=status.HTTP_201_CREATED)
async def create_participante(payload: ParticipanteCreate,db: AsyncSession = Depends(get_db))->ParticipantePublic:
    existing = await participante.get_by_telefone(db, payload.telefone)

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telephone already registered!")
    
    part =  await participante.create(
        db, 
        nome=payload.nome,
        telefone=payload.telefone,
        perfil=payload.perfil
    )

    return ParticipantePublic.model_validate(part)


@router.get("", response_model=list[ParticipantePublic])
async def list_participantes(skip:int = Query(0, ge=0),
  limit:int = Query(300, ge=1, le=1000), 
  db:AsyncSession = Depends(get_db))->list[ParticipantePublic]:

    participantes = await participante.list(db,skip=skip,limit=limit)

    return [ParticipantePublic.model_validate(part) for part in participantes]
  


@router.get("/{participante_id}", response_model=ParticipantePublic)
async def get_participante(participante_id:int,db:AsyncSession = Depends(get_db))->ParticipantePublic:
    part = await participante.get(db,participante_id)

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found!")
    return ParticipantePublic.model_validate(part)


@router.patch("/{participante_id}", response_model=ParticipantePublic)
async def update_participante(payload:ParticipanteUpdate,
    participante_id:int,
     db:AsyncSession = Depends(get_db))->ParticipantePublic:

    part = await participante.get(db,participante_id)

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found!")
    
    dados= await participante.update(
        db,
        part,
        nome=payload.nome,
        telefone=payload.telefone,
        perfil=payload.perfil
    )

    return ParticipantePublic.model_validate(dados)

@router.delete("/{participante_id}", response_model=ParticipantePublic)
async def delete_participante(participante_id:int, db:AsyncSession = Depends(get_db))->ParticipantePublic:
    part = await participante.get(db,participante_id)

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found!")

    return await participante.delete(db,part)
     

    



    


    




