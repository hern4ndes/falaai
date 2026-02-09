import argparse
import asyncio

from app.core.security import get_password_hash
from app.crud.usuario_admin import usuario_admin
from app.db.session import SessionLocal


async def create_admin(email: str, nome: str, senha: str) -> None:
    async with SessionLocal() as session:
        existing = await usuario_admin.get_by_email(session, email)
        if existing:
            raise SystemExit(f"Admin with email {email} already exists")

        await usuario_admin.create(
            session,
            email=email,
            nome=nome,
            senha_hash=get_password_hash(senha),
        )
        print(f"Admin {email} created")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("email")
    parser.add_argument("nome")
    parser.add_argument("senha")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asyncio.run(create_admin(args.email, args.nome, args.senha))


if __name__ == "__main__":
    main()
