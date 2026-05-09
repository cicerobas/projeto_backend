from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud import unit as unit_crud
from app.schemas.unit import UnitCreate, UnitRead, UnitUpdate
from app.services.auth import require_roles

router = APIRouter(prefix="/units", tags=["Unidades"])


@router.post(
    "/",
    response_model=UnitRead,
    status_code=201,
    summary="Cadastrar nova unidade na rede",
)
async def unit_create(
    unit_create: UnitCreate,
    session: SessionDep,
    current_user=Depends(require_roles("admin")),
):
    unit = unit_crud.create_unit(session, unit_create)
    return unit


@router.patch(
    "/{unit_id}", response_model=UnitRead, summary="Atualizar unidade existente"
)
async def unit_update(
    unit_id: int,
    unit_update: UnitUpdate,
    session: SessionDep,
    current_user=Depends(require_roles("admin")),
):
    unit = unit_crud.update_unit(session, unit_id, unit_update)
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    return unit


@router.delete("/{unit_id}", status_code=204, summary="Excluir unidade da rede")
async def unit_delete(
    unit_id: int,
    session: SessionDep,
    current_user=Depends(require_roles("admin")),
):
    success = unit_crud.delete_unit(session, unit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")


@router.get(
    "/{unit_id}", response_model=UnitRead, summary="Obter detalhes de uma unidade"
)
async def unit_read(unit_id: int, session: SessionDep):
    unit = unit_crud.get_unit_by_id(session, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    return unit


@router.get(
    "/", response_model=list[UnitRead], summary="Listar todas as unidades da rede"
)
async def unit_list(session: SessionDep):
    units = unit_crud.get_all_units(session)
    return units
