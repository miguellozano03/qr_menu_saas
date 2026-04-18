from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.exceptions_handlers import register_exceptions_handlers
from app.shared.storage.local_setup import init_storage, UPLOAD_DIR

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.environment == "development":
        init_storage()
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

if settings.environment == "development":
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

register_exceptions_handlers(app)
app.include_router(api_router, prefix='/api')