from uuid import UUID

from sqlmodel import Session, select

from app.schemas.user import (
    CustomerCreate,
    CustomerUpdate,
    EmployeeCreate,
    EmployeeUpdate,
)
from app.models.user import Customer, Employee
from app.core.security import get_password_hash


async def create_customer(
    session: Session, customer_create: CustomerCreate
) -> Customer:
    hashed_password = get_password_hash(customer_create.password)
    customer = Customer.model_validate(
        customer_create, update={"password_hash": hashed_password}
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


async def update_customer(
    session: Session, customer_id: UUID, customer_update: CustomerUpdate
) -> Customer | None:
    customer = session.get(Customer, customer_id)
    if not customer:
        return None

    product_data = customer_update.model_dump(exclude_unset=True)
    if "password" in product_data:
        product_data["password_hash"] = get_password_hash(product_data.pop("password"))

    customer.sqlmodel_update(product_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


async def delete_customer(session: Session, customer_id: UUID) -> bool:
    customer = session.get(Customer, customer_id)
    if not customer:
        return False

    session.delete(customer)
    session.commit()
    return True


async def create_employee(
    session: Session, employee_create: EmployeeCreate
) -> Employee:
    hashed_password = get_password_hash(employee_create.password)
    employee = Employee.model_validate(
        employee_create, update={"password_hash": hashed_password}
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


async def update_employee(
    session: Session, employee_id: UUID, employee_update: EmployeeUpdate
) -> Employee | None:
    employee = session.get(Employee, employee_id)
    if not employee:
        return None

    product_data = employee_update.model_dump(exclude_unset=True)
    if "password" in product_data:
        product_data["password_hash"] = get_password_hash(product_data.pop("password"))

    employee.sqlmodel_update(product_data)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


async def delete_employee(session: Session, employee_id: UUID) -> bool:
    employee = session.get(Employee, employee_id)
    if not employee:
        return False

    session.delete(employee)
    session.commit()
    return True


def get_customer_by_email(session: Session, email: str) -> Customer | None:
    return session.exec(select(Customer).where(Customer.email == email)).one_or_none()


def get_employee_by_email(session: Session, email: str) -> Employee | None:
    return session.exec(select(Employee).where(Employee.email == email)).one_or_none()


def get_user_by_email(session: Session, email: str) -> Customer | Employee | None:
    user = get_customer_by_email(session, email)
    if user:
        return user

    return get_employee_by_email(session, email)
