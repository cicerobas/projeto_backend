from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud import inventory as inventory_crud
from app.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate
from app.services.auth import require_roles
from app.services import inventory as inventory_service

router = APIRouter(prefix="/inventories", tags=["Estoques"])


@router.post(
    "/",
    response_model=InventoryRead,
    status_code=201,
    summary="Criar um novo registro de estoque",
)
async def inventory_create(
    inventory_create: InventoryCreate,
    session: SessionDep,
    current_user=Depends(require_roles("employee", "manager", "admin")),
):
    inventory = inventory_service.create_inventory(session, inventory_create)
    return inventory


@router.patch(
    "/{inventory_id}",
    response_model=InventoryRead,
    summary="Atualizar registro de estoque",
)
async def inventory_update(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    session: SessionDep,
    current_user=Depends(require_roles("employee", "manager", "admin")),
):
    inventory = inventory_crud.update_inventory(session, inventory_id, inventory_update)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")

    return inventory


@router.delete(
    "/{inventory_id}", status_code=204, summary="Excluir registro de estoque"
)
async def inventory_delete(
    inventory_id: int,
    session: SessionDep,
    current_user=Depends(require_roles("employee", "manager", "admin")),
):
    success = inventory_crud.delete_inventory(session, inventory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")


@router.get(
    "/{inventory_id}",
    response_model=InventoryRead,
    summary="Obter detalhes de um registro de estoque",
)
async def inventory_read(inventory_id: int, session: SessionDep):
    inventory = inventory_crud.get_inventory_by_id(session, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventário não encontrado")

    return inventory


@router.get(
    "/", response_model=list[InventoryRead], summary="Listar estoques de uma unidade"
)
async def inventory_list_by_unit(unit_id: int, session: SessionDep):
    inventories = inventory_crud.get_inventories_by_unit_id(session, unit_id)
    return inventories
