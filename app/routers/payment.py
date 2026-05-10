from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.payment import PaymentResponse
from app.services import payment as payment_service

router = APIRouter(prefix="/payments", tags=["Pagamentos"])


@router.post("/{order_id}", response_model=PaymentResponse)
def process_mock_payment(order_id: int, session: SessionDep):
    return payment_service.process_payment(session, order_id)
