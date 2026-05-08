from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    unit_id: int
    product_id: int
    total_quantity: int = Field(..., gt=0)
    reserved_quantity: int = Field(..., ge=0)


class InventoryCreate(InventoryBase):
    pass


class InventoryRead(InventoryBase):
    id: int


class InventoryUpdate(BaseModel):
    total_quantity: int | None = Field(None, gt=0)
    reserved_quantity: int | None = Field(None, ge=0)
