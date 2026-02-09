from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin
from app.core.security import get_password_hash
from app.crud.usuario_admin import usuario_admin
from app.db.session import get_db
from app.models.usuario_admin import UsuarioAdmin
from app.schemas.usuario_admin import (
    UsuarioAdminCreate,
    UsuarioAdminPublic,
    UsuarioAdminUpdate,
)

router = APIRouter(prefix="/usuarios-admin", tags=["usuarios-admin"])


@router.post("", response_model=UsuarioAdminPublic, status_code=status.HTTP_201_CREATED)
async def create_usuario_admin(
    payload: UsuarioAdminCreate,
    _: UsuarioAdmin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> UsuarioAdminPublic:
    existing = await usuario_admin.get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(payload.senha)
    admin = await usuario_admin.create(
        db,
        email=payload.email,
        senha_hash=hashed_password,
        nome=payload.nome,
    )
    return UsuarioAdminPublic.model_validate(admin)


@router.get("", response_model=list[UsuarioAdminPublic])
async def list_usuarios_admin(
    _: UsuarioAdmin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[UsuarioAdminPublic]:
    admins = await usuario_admin.list(db, skip=skip, limit=limit)
    return [UsuarioAdminPublic.model_validate(admin) for admin in admins]


@router.get("/{admin_id}", response_model=UsuarioAdminPublic)
async def get_usuario_admin(
    admin_id: int,
    _: UsuarioAdmin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> UsuarioAdminPublic:
    admin = await usuario_admin.get(db, admin_id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return UsuarioAdminPublic.model_validate(admin)


@router.patch("/{admin_id}", response_model=UsuarioAdminPublic)
async def update_usuario_admin(
    admin_id: int,
    payload: UsuarioAdminUpdate,
    _: UsuarioAdmin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> UsuarioAdminPublic:
    admin = await usuario_admin.get(db, admin_id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    update_email = payload.email
    if update_email and update_email != admin.email:
        existing = await usuario_admin.get_by_email(db, update_email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(payload.senha) if payload.senha else None

    updated_admin = await usuario_admin.update(
        db,
        admin,
        email=payload.email,
        nome=payload.nome,
        senha_hash=hashed_password,
    )
    return UsuarioAdminPublic.model_validate(updated_admin)


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario_admin(
    admin_id: int,
    _: UsuarioAdmin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> None:
    admin = await usuario_admin.get(db, admin_id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    await usuario_admin.remove(db, admin)
    return None
