from datetime import datetime, timezone
from sqlmodel import Session, select

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderChannel, OrderCreateInternal, OrderStatus


def create_order(session: Session, order_data: OrderCreateInternal) -> Order:
    try:
        total_price = 0.0
        order = Order(
            **order_data.model_dump(exclude={"items"}),
            total_price=total_price,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        session.add(order)
        session.flush()

        for item in order_data.items:
            product = session.get(Product, item.product_id)
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
            )
            total_price += round(item.quantity * product.price, 2)
            session.add(order_item)

        order.total_price = round(total_price, 2)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

    except Exception:
        session.rollback()
        raise


def update_order_status(
    session: Session, order_id: int, new_status: OrderStatus
) -> Order | None:
    order = session.get(Order, order_id)
    if not order:
        return None

    order.status = new_status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session: Session, order_id: int) -> Order | None:
    return session.get(Order, order_id)


def get_orders(
    session: Session,
    order_channel: OrderChannel | None = None,
    status: OrderStatus | None = None,
) -> list[Order]:
    query = select(Order)

    if order_channel:
        query = query.where(Order.order_channel == order_channel)
    if status:
        query = query.where(Order.status == status)

    return session.exec(query).all()
