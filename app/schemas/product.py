from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    price: float
    description: str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float):
        if v <= 0:
            raise ValueError("O preço deve ser um valor positivo.")
        return v


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float | None):
        if v is not None and v <= 0:
            raise ValueError("O preço deve ser um valor positivo.")
        return v
