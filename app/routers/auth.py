from fastapi import APIRouter
from starlette.responses import Response

from app.utils.user import *
from app.utils.utils import create_access_token

router = APIRouter()


@router.post("/register/", summary="Регистрация нового пользователя")
async def register_user(user: UserCreate, request: Request) -> dict:
    new_db_user = await create_user(user, request.state.db)
    access_token = create_access_token({"sub": str(new_db_user.id)})
    return {"msg": "User created successfully",
            "user": {"email": new_db_user.email, "username": new_db_user.username, "access_token": access_token}}


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
