from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    price: float = Field(
        ..., gt=0, description="Preço em reais, deve ser um valor positivo."
    )
    description: str | None = Field(None, max_length=300)

    @field_validator("price")
    @classmethod
    def round_price(cls, v):
        return round(v, 2)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    price: float | None = Field(
        None, gt=0, description="Preço em reais, deve ser um valor positivo."
    )
    description: str | None = Field(None, max_length=300)

    @field_validator("price")
    @classmethod
    def round_price(cls, v):
        if v is not None:
            return round(v, 2)
        return v
