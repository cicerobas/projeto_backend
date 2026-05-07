from pydantic import BaseModel


class InventoryBase(BaseModel):
    unit_id: int
    product_id: int
    total_quantity: int
    reserved_quantity: int


class InventoryCreate(InventoryBase):
    pass


class InventoryRead(InventoryBase):
    id: int


class InventoryUpdate(BaseModel):
    total_quantity: int | None = None
    reserved_quantity: int | None = None
