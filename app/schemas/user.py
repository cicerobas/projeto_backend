from uuid import UUID
from enum import Enum
from pydantic import BaseModel, field_validator, EmailStr


class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def password_minimal_size(cls, v: str):
        if len(v) < 5:
            raise ValueError("A senha deve ser maior que 5 caracteres.")
        return v


class CustomerCreate(UserCreate):
    cpf: str
    address: str | None = None

    @field_validator("cpf")
    @classmethod
    def cpf_valid(cls, v: str):
        if len(v) != 11 or not v.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return v


class EmployeeCreate(UserCreate):
    role: UserRole
    unit_id: int


class EmployeeRead(UserBase):
    id: UUID
    role: UserRole
    unit_id: int


class CustomerRead(UserBase):
    id: UUID
    cpf: str
    address: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
