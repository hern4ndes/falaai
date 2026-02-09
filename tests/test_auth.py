import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import get_password_hash
from app.crud.usuario_admin import usuario_admin


@pytest.mark.asyncio
async def test_login_returns_token(
    client: AsyncClient,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        await usuario_admin.create(
            session,
            email="admin@example.com",
            nome="Admin",
            senha_hash=get_password_hash("secret"),
        )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


@pytest.mark.asyncio
async def test_login_fails_with_bad_credentials(
    client: AsyncClient,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        await usuario_admin.create(
            session,
            email="admin@example.com",
            nome="Admin",
            senha_hash=get_password_hash("secret"),
        )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "wrong"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
