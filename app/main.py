from fastapi import FastAPI, Depends

from app.middleware.middleware import DBSessionMiddleware
from app.routers import *
from app.utils.user import get_current_user

app = FastAPI()
app.add_middleware(DBSessionMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/protected")
async def protected_route(current_user_id: str = Depends(get_current_user)):
    return {"msg": "Access granted", "user_id": current_user_id}


PROTECTED = [Depends(get_current_user)]

app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(flower_router, tags=["flowers"], prefix="/flowers")
app.include_router(user_router, tags=["users"], prefix="/users")
app.include_router(personal_flower_router, tags=["personal_flowers"], prefix="/personal_flowers")
