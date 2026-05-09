from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.crud import product as product_crud
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.auth import require_roles

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post(
    "/", response_model=ProductRead, status_code=201, summary="Cadastrar novo produto"
)
async def product_create(
    product_create: ProductCreate,
    session: SessionDep,
    current_user=Depends(require_roles("manager", "admin")),
):
    product = product_crud.create_product(session, product_create)
    return product


@router.patch("/{product_id}", response_model=ProductRead, summary="Atualizar produto")
async def product_update(
    product_id: int,
    product_update: ProductUpdate,
    session: SessionDep,
    current_user=Depends(require_roles("manager", "admin")),
):
    product = product_crud.update_product(session, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product


@router.delete("/{product_id}", status_code=204, summary="Excluir produto")
async def product_delete(
    product_id: int,
    session: SessionDep,
    current_user=Depends(require_roles("manager", "admin")),
):
    success = product_crud.delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


@router.get(
    "/{product_id}", response_model=ProductRead, summary="Obter detalhes de um produto"
)
async def product_read(product_id: int, session: SessionDep):
    product = product_crud.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product


@router.get("/", response_model=list[ProductRead], summary="Listar todos os produtos")
async def product_list(session: SessionDep):
    products = product_crud.get_all_products(session)
    return products
