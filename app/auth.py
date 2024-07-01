from typing import Any

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from app import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(connection, username: str, password: str) -> Any:
    user = crud.get_user_by_username(connection, username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> dict:
    connection = request.state.db
    user = crud.get_user_by_username(connection, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user
