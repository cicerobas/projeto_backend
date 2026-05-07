from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud.user import create_customer, create_employee, get_user_by_email
from app.schemas.user import CustomerCreate, CustomerRead, EmployeeCreate, EmployeeRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/customers/", response_model=CustomerRead, status_code=201)
async def customer_create(customer_create: CustomerCreate, session: SessionDep):
    existing_customer = get_user_by_email(session, customer_create.email)
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    customer = await create_customer(session, customer_create)
    return customer


@router.post("/employees/", response_model=EmployeeRead, status_code=201)
async def employee_create(
    employee_create: EmployeeCreate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin" and current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Acesso negado")

    existing_employee = get_user_by_email(session, employee_create.email)
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    employee = await create_employee(session, employee_create)
    return employee
