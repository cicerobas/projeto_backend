from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionDep
from app.core.security import create_access_token
from app.services.auth import authenticate_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/token", summary="Obter token de acesso")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
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
