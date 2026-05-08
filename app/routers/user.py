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
)
from app.services.auth import get_current_user

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


@router.post(
    "/employees/",
    response_model=EmployeeRead,
    status_code=201,
    summary="Cadastrar novo usuário do tipo Funcionário",
)
async def employee_create(
    employee_create: EmployeeCreate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):

    if not hasattr(current_user, "role") or (
        current_user.role != "admin" and current_user.role != "manager"
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    existing_employee = user_crud.get_user_by_email(session, employee_create.email)
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    employee = await user_crud.create_employee(session, employee_create)
    return employee
