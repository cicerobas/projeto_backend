from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import get_settings
from app.core.database import SessionDep
from app.core.security import verify_password
from app.crud.user import get_user_by_email

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


async def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user
