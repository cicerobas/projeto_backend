from sqlmodel import Session, select

from app.schemas.user import CustomerCreate, EmployeeCreate
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


def get_customer_by_email(session: Session, email: str) -> Customer | None:
    return session.exec(select(Customer).where(Customer.email == email)).one_or_none()


def get_employee_by_email(session: Session, email: str) -> Employee | None:
    return session.exec(select(Employee).where(Employee.email == email)).one_or_none()


def get_user_by_email(session: Session, email: str) -> Customer | Employee | None:
    user = get_customer_by_email(session, email)
    if user:
        return user

    return get_employee_by_email(session, email)
