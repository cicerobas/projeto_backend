from uuid import UUID
from enum import Enum
from pydantic import BaseModel, field_validator, EmailStr, Field


class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(..., max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=5, max_length=50)


class CustomerCreate(UserCreate):
    cpf: str = Field(..., max_length=11)
    address: str | None = Field(None, max_length=200)

    @field_validator("cpf")
    @classmethod
    def cpf_valid(cls, v: str):
        if len(v) != 11 or not v.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return v


class CustomerUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=5, max_length=50)
    address: str | None = Field(None, max_length=200)


class EmployeeCreate(UserCreate):
    role: UserRole = Field(
        ..., description="O cargo do funcionário (employee, manager ou admin)."
    )
    unit_id: int


class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=5, max_length=50)
    role: UserRole | None = Field(
        None, description="O cargo do funcionário (employee, manager ou admin)."
    )
    unit_id: int | None = Field(None)


class EmployeeRead(UserBase):
    id: UUID
    role: UserRole
    unit_id: int


class CustomerRead(UserBase):
    id: UUID
    cpf: str
    address: str | None = None
