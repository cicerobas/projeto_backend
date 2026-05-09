from fastapi import APIRouter, Depends, Query

from app.core.database import SessionDep
from app.models.user import Customer, Employee
from app.schemas.order import OrderCreate, OrderCreateTotem, OrderRead
from app.services import order as order_service
from app.services.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.post(
    "/", status_code=201, response_model=OrderRead, summary="Criar um novo pedido"
)
async def create_order(
    order_data: OrderCreate,
    session: SessionDep,
    current_user: Customer | Employee = Depends(get_current_user),
    customer_cpf: str | None = Query(
        default=None,
        description="CPF do cliente (para 'in_store' e 'totem')",
    ),
):
    return order_service.create_order(session, order_data, current_user, customer_cpf)


@router.post(
    "/totem",
    status_code=201,
    response_model=OrderRead,
    summary="Criar pedido via totem",
)
async def create_order_totem(
    order_data: OrderCreateTotem,
    session: SessionDep,
    customer_cpf: str | None = Query(
        default=None,
        description="CPF do cliente (para 'in_store' e 'totem')",
    ),
):
    return order_service.create_order_totem(session, order_data, customer_cpf)
