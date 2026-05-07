from sqlmodel import SQLModel, Field


class Inventory(SQLModel, table=True):
    __tablename__ = "inventories"

    id: int | None = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="units.id")
    product_id: int = Field(foreign_key="products.id")
    total_quantity: int = Field(nullable=False, default=0)
    reserved_quantity: int = Field(nullable=False, default=0)
