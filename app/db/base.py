from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models."""


# Import models here so Alembic has access to metadata.
from app import models  # noqa: E402,F401
