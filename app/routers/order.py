from fastapi import APIRouter, Depends, Query

from app.core.database import SessionDep
from app.models.user import Customer, Employee
from app.schemas import order as order_schemas
from app.services import order as order_service
from app.crud import order as order_crud
from app.services.auth import get_current_user, require_roles

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.post(
    "/",
    status_code=201,
    response_model=order_schemas.OrderRead,
    summary="Criar um novo pedido",
)
async def create_order(
    order_data: order_schemas.OrderCreate,
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
    response_model=order_schemas.OrderRead,
    summary="Criar pedido via totem",
)
async def create_order_totem(
    order_data: order_schemas.OrderCreateTotem,
    session: SessionDep,
    customer_cpf: str | None = Query(
        default=None,
        description="CPF do cliente (para 'in_store' e 'totem')",
    ),
):
    return order_service.create_order_totem(session, order_data, customer_cpf)


@router.get(
    "/",
    response_model=list[order_schemas.OrderRead],
    summary="Listar pedidos com filtros opcionais",
)
def get_orders(
    session: SessionDep,
    order_channel: order_schemas.OrderChannel | None = Query(default=None),
    status: order_schemas.OrderStatus | None = Query(default=None),
):
    return order_crud.get_orders(session, order_channel, status)


@router.patch(
    "/{order_id}/status",
    response_model=order_schemas.OrderRead,
    summary="Atualizar status de um pedido",
)
def update_order_status(
    session: SessionDep,
    order_id: int,
    new_status: order_schemas.OrderStatus = Query(...),
    current_user=Depends(require_roles("employee", "manager", "admin")),
):
    return order_service.update_order_status(session, order_id, new_status)
