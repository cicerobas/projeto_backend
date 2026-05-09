from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    unit_id: int = Field(nullable=False, foreign_key="units.id")
    customer_id: UUID = Field(nullable=True, foreign_key="customers.id")
    employee_id: UUID = Field(nullable=True, foreign_key="employees.id")
    status: str = Field(nullable=False)
    total_price: float = Field(nullable=False)
    order_channel: str = Field(nullable=False)
    payment_method: str = Field(nullable=False)
    created_at: str = Field(nullable=False)

    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(nullable=False, foreign_key="orders.id")
    product_id: int = Field(nullable=False, foreign_key="products.id")
    quantity: int = Field(nullable=False)
    unit_price: float = Field(nullable=False)

    order: Order = Relationship(back_populates="items")
