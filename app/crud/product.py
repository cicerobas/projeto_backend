from sqlmodel import Session, select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(session: Session, product_create: ProductCreate) -> Product:
    product = Product.model_validate(product_create)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(
    session: Session, product_id: int, product_update: ProductUpdate
) -> Product | None:
    product = session.get(Product, product_id)
    if not product:
        return None

    product_data = product_update.model_dump(exclude_unset=True)
    product.sqlmodel_update(product_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: Session, product_id: int) -> bool:
    product = session.get(Product, product_id)
    if not product:
        return False

    session.delete(product)
    session.commit()
    return True


def get_product_by_id(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)

def get_all_products(session: Session) -> list[Product]:
    return session.exec(select(Product)).all()
