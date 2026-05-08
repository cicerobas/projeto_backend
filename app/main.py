from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_db_and_tables, seed_db
from app.routers import auth, user, product, unit, inventory


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="API Raizes do Nordeste",
    version="0.1.0",
    contact={"name": "Cicero Simões", "email": "cbruno.dev@gmail.com"},
)
app.include_router(auth.router)
app.include_router(unit.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(inventory.router)
