from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud.inventory import (
    get_inventory_by_id,
    get_inventories_by_unit_id,
    update_inventory,
    delete_inventory,
)
from app.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate
from app.services.auth import get_current_user
from app.services import inventory as inventory_service

router = APIRouter(prefix="/inventories", tags=["inventories"])


@router.post("/", response_model=InventoryRead, status_code=201)
async def inventory_create(
    inventory_create: InventoryCreate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if (
        current_user.role != "manager"
        and current_user.role != "employee"
        and current_user.role != "admin"
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    inventory = inventory_service.create_inventory(session, inventory_create)
    return inventory


@router.patch("/{inventory_id}", response_model=InventoryRead)
async def inventory_update(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if (
        current_user.role != "manager"
        and current_user.role != "employee"
        and current_user.role != "admin"
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    inventory = update_inventory(session, inventory_id, inventory_update)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")

    return inventory


@router.delete("/{inventory_id}", status_code=204)
async def inventory_delete(
    inventory_id: int,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if (
        current_user.role != "manager"
        and current_user.role != "employee"
        and current_user.role != "admin"
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    success = delete_inventory(session, inventory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")


@router.get("/{inventory_id}", response_model=InventoryRead)
async def inventory_read(inventory_id: int, session: SessionDep):
    inventory = get_inventory_by_id(session, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")

    return inventory


@router.get("/", response_model=list[InventoryRead])
async def inventory_list_by_unit(unit_id: int, session: SessionDep):
    inventories = get_inventories_by_unit_id(session, unit_id)
    return inventories
