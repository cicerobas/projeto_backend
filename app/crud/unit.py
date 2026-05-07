from sqlmodel import Session, select

from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate


def create_unit(session: Session, unit_create: UnitCreate) -> Unit:
    unit = Unit.model_validate(unit_create)
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit


def update_unit(session: Session, unit_id: int, unit_update: UnitUpdate) -> Unit | None:
    unit = session.get(Unit, unit_id)
    if not unit:
        return None

    unit_data = unit_update.model_dump(exclude_unset=True)
    unit.sqlmodel_update(unit_data)
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit


def delete_unit(session: Session, unit_id: int) -> bool:
    unit = session.get(Unit, unit_id)
    if not unit:
        return False

    session.delete(unit)
    session.commit()
    return True


def get_unit_by_id(session: Session, unit_id: int) -> Unit | None:
    return session.get(Unit, unit_id)


def get_all_units(session: Session) -> list[Unit]:
    return session.exec(select(Unit)).all()
