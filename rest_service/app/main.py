from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)
add_pagination(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(api_router)
