from sqlmodel import Session, select

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate


def create_inventory(session: Session, inventory_create: InventoryCreate) -> Inventory:
    inventory = Inventory.model_validate(inventory_create)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


def update_inventory(
    session: Session, inventory_id: int, inventory_update: InventoryUpdate
) -> Inventory | None:
    inventory = session.get(Inventory, inventory_id)
    if not inventory:
        return None

    inventory_data = inventory_update.model_dump(exclude_unset=True)
    inventory.sqlmodel_update(inventory_data)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


def delete_inventory(session: Session, inventory_id: int) -> bool:
    inventory = session.get(Inventory, inventory_id)
    if not inventory:
        return False

    session.delete(inventory)
    session.commit()
    return True


def get_inventory_by_id(session: Session, inventory_id: int) -> Inventory | None:
    return session.get(Inventory, inventory_id)


def get_inventories_by_unit_id(session: Session, unit_id: int) -> list[Inventory]:
    return session.exec(select(Inventory).where(Inventory.unit_id == unit_id)).all()
