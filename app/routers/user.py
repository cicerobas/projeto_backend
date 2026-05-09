from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud import user as user_crud
from app.schemas.user import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
)
from app.services.auth import get_current_user, require_roles

router = APIRouter(prefix="/user", tags=["Usuários"])


@router.post(
    "/customers/",
    response_model=CustomerRead,
    status_code=201,
    summary="Cadastrar novo usuário do tipo Cliente",
)
async def customer_create(customer_create: CustomerCreate, session: SessionDep):
    existing_customer = user_crud.get_user_by_email(session, customer_create.email)
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    customer = await user_crud.create_customer(session, customer_create)
    return customer


@router.patch(
    "/customers/me",
    response_model=CustomerRead,
    summary="Atualizar dados do Cliente",
)
async def customer_update(
    customer_update: CustomerUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    customer = await user_crud.update_customer(
        session, current_user.id, customer_update
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.delete(
    "/customers/me",
    status_code=204,
    summary="Excluir cliente",
)
async def customer_delete(
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    success = await user_crud.delete_customer(session, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")


@router.get(
    "customers/me", response_model=CustomerRead, summary="Obter dados do cliente logado"
)
async def get_current_customer(
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    customer = await user_crud.get_customer(session, current_user.id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.post(
    "/employees/",
    response_model=EmployeeRead,
    status_code=201,
    summary="Cadastrar novo usuário do tipo Funcionário",
)
async def employee_create(
    employee_create: EmployeeCreate,
    session: SessionDep,
    current_user=Depends(require_roles("admin", "manager")),
):
    existing_employee = user_crud.get_user_by_email(session, employee_create.email)
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    employee = await user_crud.create_employee(session, employee_create)
    return employee


@router.patch(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    summary="Atualizar dados do Funcionário",
)
async def employee_update(
    employee_id: UUID,
    employee_update: EmployeeUpdate,
    session: SessionDep,
    current_user=Depends(require_roles("admin", "manager")),
):
    employee = await user_crud.update_employee(session, employee_id, employee_update)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.delete(
    "/employees/{employee_id}",
    status_code=204,
    summary="Excluir funcionário",
)
async def employee_delete(
    employee_id: UUID,
    session: SessionDep,
    current_user=Depends(require_roles("admin", "manager")),
):
    success = await user_crud.delete_employee(session, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
