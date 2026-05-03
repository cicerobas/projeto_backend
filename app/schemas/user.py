from enum import Enum
from pydantic import BaseModel, field_validator, EmailStr


class UserRole(Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


class UserBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(UserBase):
    password: str
    cpf: str
    address: str | None = None

    @field_validator("password")
    def password_minimal_size(cls, v: str):
        if len(v) < 5:
            raise ValueError("A senha deve ser maior que 5 caracteres.")
        return v

    @field_validator("cpf")
    def cpf_valid(cls, v: str):
        if len(v) != 11 or not v.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return v


class EmployeeCreate(UserBase):
    password: str
    role: UserRole

    @field_validator("password")
    def password_minimal_size(cls, v: str):
        if len(v) < 5:
            raise ValueError("A senha deve ser maior que 5 caracteres.")
        return v


class EmployeeRead(UserBase):
    role: UserRole


class CustomerRead(UserBase):
    cpf: str
    address: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
