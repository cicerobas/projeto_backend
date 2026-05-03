from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.core.security import create_access_token
from app.schemas.user import UserLogin
from app.services.auth import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(session: SessionDep, login_data: UserLogin):
    user = await authenticate_user(session, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data: dict = {"sub": str(user.email)}
    if hasattr(user, "role"):
        token_data["role"] = user.role

    token = create_access_token(token_data)

    return {"access_token": token, "token_type": "bearer"}
