from datetime import datetime, timezone
from sqlmodel import Session

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreateInternal


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
