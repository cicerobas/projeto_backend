from uuid import UUID

from sqlmodel import Session, select

from app.models.payment import Payment


def create_payment(session: Session, payment: Payment) -> Payment:
    try:
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment
    except Exception:
        session.rollback()
        raise


def get_payment_by_order_id(session: Session, order_id: int) -> Payment | None:
    return session.exec(select(Payment).where(Payment.order_id == order_id)).first()


def get_payment_by_transaction_id(session: Session, transaction_id: UUID) -> Payment | None:
    return session.exec(select(Payment).where(Payment.transaction_id == transaction_id)).first()