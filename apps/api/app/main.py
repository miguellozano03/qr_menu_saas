from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.db import models
from app.core.exceptions_handlers import register_exceptions_handlers

app = FastAPI(title=settings.app_name)
register_exceptions_handlers(app)
app.include_router(api_router)