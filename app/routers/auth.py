from fastapi import APIRouter
from starlette.requests import Request
from app.schemas.user import UserCreate, LoginRequest
from app.utils.user import *
from app.utils.utils import create_access_token

route = APIRouter()


@route.post("/register/", summary="Register new user")
async def register_user(user: UserCreate, request: Request):
    new_db_user = await create_user(user, request.state.db)
    access_token = create_access_token({"sub": str(user.id)})
    return {"msg": "User created successfully", "user": {"email": new_db_user.email, "username": new_db_user.username, "access_token": access_token}}


@route.post("/login/", summary="Login user")
async def login_user(user: LoginRequest, request: Request):
    user = await authenticate_user(user, request.state.db)
    access_token = create_access_token({"sub": str(user.id)})
    return {"msg": "User logged in successfully", "user": {"email": user.email, "username": user.username, "access_token": access_token}}

