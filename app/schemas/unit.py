from pydantic import BaseModel, field_validator


class UnitBase(BaseModel):
    name: str
    cnpj: str
    address: str

    @field_validator("cnpj")
    @classmethod
    def cnpj_valid(cls, v: str):
        if len(v) != 14 or not v.isdigit():
            raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos.")
        return v


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    name: str | None = None
    cnpj: str | None = None
    address: str | None = None

    @field_validator("cnpj")
    @classmethod
    def cnpj_valid(cls, v: str):
        if v is not None and (len(v) != 14 or not v.isdigit()):
            raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos.")
        return v


class UnitPublic(UnitBase):
    id: int
