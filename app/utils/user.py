from datetime import datetime, timezone
from typing import Annotated

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.DAO.base import UserDAO
from app.models import User
from app.schemas.user import UserCreate, LoginRequest
from app.utils.utils import hash_password, verify_password, verify_access_token


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    """
    Создает нового пользователя в базе данных.
    """
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        city=user.city,
        info=user.info,
        photo=user.photo,
    )

    try:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await session.rollback()
        if 'email' in str(e.orig):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        elif 'username' in str(e.orig):
            raise HTTPException(status_code=400, detail="User with this username already exists")
        else:
            raise HTTPException(status_code=400, detail="Error occurred while creating user")
token_bearer = HTTPBearer()
token_verify = Annotated[HTTPAuthorizationCredentials, Depends(token_bearer)]

async def get_access_token(request: Request, token: HTTPAuthorizationCredentials = Depends(token_bearer)) -> str:
    """
    Проверяет токен на истечение срока действия и возвращает его.
    """
    token = token.credentials  # Получаем сам токен из переданных данных.
    try:
        payload = verify_access_token(token)  # Верификация токена
        expire = payload.get("exp")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if expire:
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if expire_time < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

    return token


async def authenticate_user(user: LoginRequest, session: AsyncSession) -> User:
    """
    Аутентификация пользователя. (логин)
    """
    result = await session.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(provided_password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return db_user




async def get_current_user(request: Request, token: str = Depends(get_access_token)):
    try:
        payload = verify_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=401, detail="Token expired")

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found in token")

    user = await UserDAO.find_one_or_none_by_id(int(user_id), request.state.db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

current_user = Annotated[User, Depends(get_current_user)]
