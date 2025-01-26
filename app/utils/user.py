from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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


async def authenticate_user(user: LoginRequest, session: AsyncSession) -> User:
    """
    Аутентификация пользователя. (логин)
    """
    result = await session.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(provided_password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return db_user


security = HTTPBearer()


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    return user_id
