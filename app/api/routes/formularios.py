import json

import jsonschema
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import BASE_DIR
from app.crud.formulario import formulario_crud
from app.db.session import get_db
from app.schemas.formulario import (
    FormularioCreate,
    FormularioPublic,
    FormularioUpdate,
)

router = APIRouter(prefix="/formularios", tags=["formularios"])

_META_SCHEMA_PATH = BASE_DIR / "FalaAiMetaSchema.json"
with open(_META_SCHEMA_PATH) as f:
    _META_SCHEMA = json.load(f)


def _validate_against_meta_schema(data: dict) -> None:
    try:
        jsonschema.validate(instance=data, schema=_META_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"formulario_json nao e valido segundo o MetaSchema: {exc.message}",
        )


@router.post("", response_model=FormularioPublic, status_code=status.HTTP_201_CREATED)
async def create_formulario(
    payload: FormularioCreate,
    db: AsyncSession = Depends(get_db),
) -> FormularioPublic:
    _validate_against_meta_schema(payload.formulario_json)

    formulario = await formulario_crud.create(
        db,
        formulario_json=payload.formulario_json,
        status=payload.status,
    )
    return FormularioPublic.model_validate(formulario)


@router.get("", response_model=list[FormularioPublic])
async def list_formularios(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[FormularioPublic]:
    formularios = await formulario_crud.list(db, skip=skip, limit=limit)
    return [FormularioPublic.model_validate(f) for f in formularios]


@router.get("/{formulario_id}", response_model=FormularioPublic)
async def get_formulario(
    formulario_id: int,
    db: AsyncSession = Depends(get_db),
) -> FormularioPublic:
    formulario = await formulario_crud.get(db, formulario_id)
    if formulario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Formulario nao encontrado"
        )
    return FormularioPublic.model_validate(formulario)


@router.patch("/{formulario_id}", response_model=FormularioPublic)
async def update_formulario(
    formulario_id: int,
    payload: FormularioUpdate,
    db: AsyncSession = Depends(get_db),
) -> FormularioPublic:
    formulario = await formulario_crud.get(db, formulario_id)
    if formulario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Formulario nao encontrado"
        )

    if payload.formulario_json is not None:
        _validate_against_meta_schema(payload.formulario_json)

    updated = await formulario_crud.update(
        db,
        formulario,
        formulario_json=payload.formulario_json,
        status=payload.status,
    )
    return FormularioPublic.model_validate(updated)


@router.delete("/{formulario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_formulario(
    formulario_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    formulario = await formulario_crud.get(db, formulario_id)
    if formulario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Formulario nao encontrado"
        )

    await formulario_crud.remove(db, formulario)
    return None
