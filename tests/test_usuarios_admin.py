import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import get_password_hash
from app.crud.usuario_admin import usuario_admin


@pytest.mark.asyncio
async def test_admin_crud_flow(
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

    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "secret"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = await client.post(
        "/api/v1/usuarios-admin",
        json={"email": "user1@example.com", "nome": "User One", "senha": "password1"},
        headers=headers,
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["email"] == "user1@example.com"

    list_response = await client.get("/api/v1/usuarios-admin", headers=headers)
    assert list_response.status_code == 200
    emails = [item["email"] for item in list_response.json()]
    assert "admin@example.com" in emails
    assert "user1@example.com" in emails

    update_response = await client.patch(
        f"/api/v1/usuarios-admin/{created['id']}",
        json={"nome": "User One Updated"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["nome"] == "User One Updated"

    delete_response = await client.delete(
        f"/api/v1/usuarios-admin/{created['id']}",
        headers=headers,
    )
    assert delete_response.status_code == 204

    list_after_delete = await client.get("/api/v1/usuarios-admin", headers=headers)
    remaining_emails = [item["email"] for item in list_after_delete.json()]
    assert "user1@example.com" not in remaining_emails
