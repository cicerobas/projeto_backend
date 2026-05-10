from fastapi import HTTPException
from sqlmodel import Session

from app.crud import order as order_crud
from app.models.order import Order
from app.models.user import Customer, Employee
from app.schemas.order import (
    OrderCreate,
    OrderCreateInternal,
    OrderCreateTotem,
    OrderStatus,
)
from app.schemas.inventory import InventoryUpdate
from app.crud import user as user_crud
from app.crud import product as product_crud
from app.crud import inventory as inventory_crud
from app.crud import unit as unit_crud


def check_order_items(session: Session, order_data: OrderCreateInternal):
    for item in order_data.items:
        product = product_crud.get_product_by_id(session, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Produto com ID {item.product_id} não encontrado.",
            )
        inventory = inventory_crud.get_inventory_by_product_and_unit(
            session, item.product_id, order_data.unit_id
        )
        if (
            not inventory
            or (inventory.total_quantity - inventory.reserved_quantity) < item.quantity
        ):
            unit = unit_crud.get_unit_by_id(session, order_data.unit_id)
            raise HTTPException(
                status_code=409,
                detail=f"Estoque insuficiente para o produto: {product.name} na unidade {unit.name}.",
            )

        inventory_crud.update_inventory(
            session,
            inventory.id,
            InventoryUpdate(
                reserved_quantity=inventory.reserved_quantity + item.quantity
            ),
        )


def create_order(
    session: Session,
    order_data: OrderCreate,
    current_user: Customer | Employee,
    customer_cpf: str | None = None,
) -> Order:

    order_internal = OrderCreateInternal(**order_data.model_dump())

    if order_internal.order_channel in ["app", "web", "pickup"]:
        if not isinstance(current_user, Customer):
            raise HTTPException(
                status_code=403, detail="Este canal exige um cliente autenticado."
            )
        order_internal.customer_id = current_user.id

    elif order_internal.order_channel in ["in_store"]:
        if not isinstance(current_user, Employee):
            raise HTTPException(
                status_code=403, detail="Este canal exige um funcionário autenticado."
            )
        order_internal.employee_id = current_user.id

        if customer_cpf:
            customer = user_crud.get_customer_by_cpf(session, customer_cpf)
            if not customer:
                raise HTTPException(
                    status_code=404,
                    detail="Cliente não encontrado com o CPF informado.",
                )
            order_internal.customer_id = customer.id

    else:
        raise HTTPException(
            status_code=400, detail=f"Canal '{order_internal.order_channel}' inválido."
        )

    check_order_items(session, order_internal)
    return order_crud.create_order(session, order_internal)


def create_order_totem(
    session: Session,
    order_data: OrderCreateTotem,
    customer_cpf: str | None = None,
) -> Order:
    order_internal = OrderCreateInternal(**order_data.model_dump())

    if order_internal.order_channel != "totem":
        raise HTTPException(
            status_code=400, detail="Rota exclusiva para canal 'totem'."
        )

    if customer_cpf:
        customer = user_crud.get_customer_by_cpf(session, customer_cpf)
        if not customer:
            raise HTTPException(
                status_code=404, detail="Cliente não encontrado com o CPF informado."
            )
        order_internal.customer_id = customer.id

    check_order_items(session, order_internal)
    return order_crud.create_order(session, order_internal)


def update_order_status(
    session: Session, order_id: int, new_status: OrderStatus
) -> Order:
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if new_status in [OrderStatus.COMPLETED, OrderStatus.CANCELED]:
        update_inventory_quantity(
            session, order, is_cancellation=(new_status == OrderStatus.CANCELED)
        )

    return order_crud.update_order_status(session, order_id, new_status)


def update_inventory_quantity(
    session: Session, order: Order, is_cancellation: bool = False
):
    for item in order.items:
        inventory = inventory_crud.get_inventory_by_product_and_unit(
            session, item.product_id, order.unit_id
        )
        if inventory:
            new_reserved = inventory.reserved_quantity - item.quantity
            new_total = (
                inventory.total_quantity
                if is_cancellation
                else inventory.total_quantity - item.quantity
            )
            inventory_crud.update_inventory(
                session,
                inventory.id,
                InventoryUpdate(
                    reserved_quantity=new_reserved, total_quantity=new_total
                ),
            )
