from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserBase(SQLModel):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False)


class Customer(UserBase, table=True):
    __tablename__ = "customers"

    cpf: str = Field(unique=True)
    address: str | None = None


class Employee(UserBase, table=True):
    __tablename__ = "employees"

    role: str = Field(nullable=False)
    unit_id: int | None = Field(default=None, foreign_key="units.id", nullable=True)
