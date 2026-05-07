from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud.unit import (
    create_unit,
    get_all_units,
    update_unit,
    delete_unit,
    get_unit_by_id,
)
from app.schemas.unit import UnitCreate, UnitRead, UnitUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/units", tags=["units"])


@router.post("/", response_model=UnitRead, status_code=201)
async def unit_create(
    unit_create: UnitCreate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    unit = create_unit(session, unit_create)
    return unit


@router.patch("/{unit_id}", response_model=UnitRead)
async def unit_update(
    unit_id: int,
    unit_update: UnitUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    unit = update_unit(session, unit_id, unit_update)
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    return unit


@router.delete("/{unit_id}", status_code=204)
async def unit_delete(
    unit_id: int,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    success = delete_unit(session, unit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")


@router.get("/{unit_id}", response_model=UnitRead)
async def unit_read(unit_id: int, session: SessionDep):
    unit = get_unit_by_id(session, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    return unit


@router.get("/", response_model=list[UnitRead])
async def unit_list(session: SessionDep):
    units = get_all_units(session)
    return units
