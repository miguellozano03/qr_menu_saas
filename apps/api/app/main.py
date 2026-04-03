from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "version": 1.00
    }