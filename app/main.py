from fastapi import FastAPI

from app.middleware.middleware import DBSessionMiddleware

app = FastAPI()
app.add_middleware(DBSessionMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}
