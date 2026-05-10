from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    status: str = Field(nullable=False)
    method: str = Field(nullable=False)
    total_amount: float = Field(gt=0, nullable=False)
    transaction_id: UUID = Field(nullable=False, unique=True)
    payload: str = Field(nullable=False)
    created_at: str = Field(nullable=False)
