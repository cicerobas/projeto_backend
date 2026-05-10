from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class OrderChannel(str, Enum):
    APP = "app"
    WEB = "web"
    PICKUP = "pickup"
    TOTEM = "totem"
    IN_STORE = "in_store"


class PaymentMethod(str, Enum):
    MOCK = "mock"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., description="ID do produto.")
    quantity: int = Field(..., gt=0)


class OrderItemRead(OrderItemBase):
    product_id: int = Field(..., description="ID do produto.")


class OrderBase(BaseModel):
    unit_id: int = Field(..., description="ID da unidade onde o pedido foi realizado.")
    order_channel: OrderChannel = Field(
        ..., description="Canal pelo qual o pedido foi realizado."
    )
    payment_method: PaymentMethod = Field(
        ..., description="Método de pagamento utilizado no pedido."
    )


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(
        ..., description="Lista de itens que compõem o pedido."
    )


class OrderCreateTotem(OrderCreate):
    order_channel: OrderChannel = OrderChannel.TOTEM


class OrderCreateInternal(OrderCreate):
    status: OrderStatus = OrderStatus.PENDING
    customer_id: UUID | None = None
    employee_id: UUID | None = None


class OrderRead(OrderBase):
    id: int
    status: OrderStatus
    total_price: float = Field(..., gt=0, description="Preço total do pedido em reais.")
    items: list[OrderItemCreate] = Field(
        ..., description="Lista de itens que compõem o pedido."
    )
    created_at: str = Field(..., description="Data e hora de criação do pedido.")


class OrderUpdateStatus(BaseModel):
    status: OrderStatus
