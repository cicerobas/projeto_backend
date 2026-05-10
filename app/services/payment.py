from datetime import datetime, timezone
from enum import Enum
import json
import random
from uuid import uuid4

from fastapi import HTTPException
from sqlmodel import Session

from app.models.payment import Payment
from app.crud import order as order_crud
from app.crud import payment as payment_crud
from app.schemas.order import OrderStatus, PaymentMethod
from app.services import order as order_service


class PaymentStatus(str, Enum):
    APPROVED = "approved"
    DECLINED = "declined"


def mock_payment_gateway(method: str, total_amount: float) -> dict:
    approved = random.random() > 0.2
    return {
        "transaction_id": uuid4(),
        "status": PaymentStatus.APPROVED if approved else PaymentStatus.DECLINED,
        "method": method,
        "total_amount": total_amount,
        "gateway": "mock",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def process_payment(session: Session, order_id: int) -> Payment:
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Pagamento só pode ser processado para pedidos pendentes.",
        )

    gateway_response = mock_payment_gateway(
        method=PaymentMethod.MOCK.value, total_amount=order.total_price
    )

    payment = Payment(
        order_id=order_id,
        status=gateway_response["status"],
        method=gateway_response["method"],
        total_amount=gateway_response["total_amount"],
        transaction_id=gateway_response["transaction_id"],
        payload=json.dumps(gateway_response, default=str),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    payment_crud.create_payment(session, payment)

    status = OrderStatus.PROCESSING if payment.status == PaymentStatus.APPROVED else OrderStatus.CANCELED
    order_service.update_order_status(session, order_id, status)

    return payment