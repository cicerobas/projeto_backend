from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud.product import (
    create_product,
    get_all_products,
    update_product,
    delete_product,
    get_product_by_id,
)
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRead, status_code=201)
async def product_create(
    product_create: ProductCreate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    product = create_product(session, product_create)
    return product


@router.patch("/{product_id}", response_model=ProductRead)
async def product_update(
    product_id: int,
    product_update: ProductUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    product = update_product(session, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product


@router.delete("/{product_id}", status_code=204)
async def product_delete(
    product_id: int,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    success = delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


@router.get("/{product_id}", response_model=ProductRead)
async def product_read(product_id: int, session: SessionDep):
    product = get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product


@router.get("/", response_model=list[ProductRead])
async def product_list(session: SessionDep):
    products = get_all_products(session)
    return products
