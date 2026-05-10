from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi import Depends

from app.core.config import get_settings
from app.core.security import get_password_hash
from app import models

settings = get_settings()

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def seed_db():
    with Session(engine) as session:
        admin = session.exec(
            select(models.Employee).where(models.Employee.email == settings.ADMIN_EMAIL)
        ).one_or_none()
        if not admin:
            admin = models.Employee(
                name="Admin",
                email=settings.ADMIN_EMAIL,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                role="admin",
            )
            session.add(admin)
            session.commit()
