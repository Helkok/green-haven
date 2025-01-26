from fastapi import FastAPI, Depends

from app.middleware.middleware import DBSessionMiddleware
from app.routers import auth_route
from app.routers import flower_route
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

app.include_router(auth_route, tags=["auth"], prefix="/auth")
app.include_router(flower_route, tags=["flowers"], prefix="/flowers")
