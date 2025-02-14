from fastapi import APIRouter
from starlette.responses import Response

from app.api.dependencies import *
from app.core.security import create_access_token, hash_password
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, request: Request):
    """
    Регистрирует нового пользователя.
    """
    hashed_password = hash_password(user.password)  # Хэшируем пароль
    new_db_user = await UserDAO.add(
        request.state.db,
        username=user.username,
        email=user.email,
        password=hashed_password,
        city=user.city,
        info=user.info,
        photo=user.photo
    )
    return {"token": create_access_token({"sub": new_db_user.username})}


@router.post("/login/", summary="Авторизация пользователя")
async def login_user(user: LoginRequest, request: Request, response: Response) -> dict:
    db_user = await authenticate_user(user, request.state.db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(db_user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {"msg": "User logged in successfully",
            "user": {"username": db_user.username, "email": db_user.email, "access_token": access_token}}


@router.post("/logout/", summary="Выход из системы")
async def logout_user(response: Response, token: token_verify) -> dict:
    response.delete_cookie(key="access_token")
    return {"msg": "User logged out successfully"}


@router.post("/refresh/", summary="Обновление токена")
async def refresh_token(response: Response, token: token_verify) -> dict:
    decoded_token = verify_access_token(token.credentials)
    sub = decoded_token.get("sub")
    if not sub:
        raise HTTPException(status_code=400, detail="Token does not contain 'sub' field")

    access_token = create_access_token({"sub": sub})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {"msg": "Token refreshed successfully"}
