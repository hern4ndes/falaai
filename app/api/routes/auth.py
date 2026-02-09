from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.crud.usuario_admin import usuario_admin
from app.db.session import get_db
from app.schemas.usuario_admin import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    admin = await usuario_admin.get_by_email(db, form_data.username)
    if admin is None or not verify_password(form_data.password, admin.senha_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = create_access_token(subject=admin.email)
    return Token(access_token=access_token)
