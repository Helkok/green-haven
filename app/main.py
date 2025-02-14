from fastapi import FastAPI

from app.api.main import api_router
from app.middleware.middleware import DBSessionMiddleware
from app.utils.constants import DESCRIPTION_APP

app = FastAPI(title="Flowers API", summary="Flowers API", version="0.1.0", description=DESCRIPTION_APP)
app.add_middleware(DBSessionMiddleware)

app.include_router(api_router, prefix="/api")
