from fastapi import HTTPException
from sqlmodel import Session

from app.crud import inventory as inventory_crud
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.unit import Unit
from app.schemas.inventory import InventoryCreate


def create_inventory(
    session: Session, inventory_create: InventoryCreate
) -> Inventory:
    unit = session.get(Unit, inventory_create.unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    product = session.get(Product, inventory_create.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return inventory_crud.create_inventory(session, inventory_create)
