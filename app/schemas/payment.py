from uuid import UUID

from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    order_id: int
    status: str
    method: str
    total_amount: float = Field(gt=0)
    transaction_id: UUID
    payload: str


class PaymentResponse(PaymentBase):
    id: UUID
    created_at: str
