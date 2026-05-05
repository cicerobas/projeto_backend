from sqlmodel import SQLModel, Field


class Unit(SQLModel, table=True):
    __tablename__ = "units"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    cnpj: str = Field(nullable=False, unique=True)
    address: str = Field(nullable=False)
