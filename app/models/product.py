from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = None
    price: float = Field(nullable=False)