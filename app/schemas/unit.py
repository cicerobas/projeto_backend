from pydantic import BaseModel, Field, field_validator


class UnitBase(BaseModel):
    name: str = Field(..., max_length=100)
    cnpj: str = Field(..., max_length=14)
    address: str = Field(..., max_length=200)

    @field_validator("cnpj")
    @classmethod
    def cnpj_valid(cls, v: str):
        if len(v) != 14 or not v.isdigit():
            raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos.")
        return v


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    name: str | None = Field(None, max_length=100)
    cnpj: str | None = Field(None, max_length=14)
    address: str | None = Field(None, max_length=200)

    @field_validator("cnpj")
    @classmethod
    def cnpj_valid(cls, v: str):
        if v is not None and (len(v) != 14 or not v.isdigit()):
            raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos.")
        return v


class UnitRead(UnitBase):
    id: int
