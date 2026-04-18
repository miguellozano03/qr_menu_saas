import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.exceptions_handlers import register_exceptions_handlers
from app.shared.storage.local_setup import init_storage, UPLOAD_DIR


# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    if settings.environment == "development":
        init_storage()
    yield
    logger.info("Shutting down...")

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get("/ping")
async def ping():
    return {"pong": True}

# --- Middlewares ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # pyright: ignore[reportArgumentType]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.environment == "development":
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

register_exceptions_handlers(app)
app.include_router(api_router, prefix="/api")

