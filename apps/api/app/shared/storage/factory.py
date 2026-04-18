from app.core.config import settings
from .local import LocalStorageService
from .r2 import R2StorageService
from .base import StorageService

def get_storage(folder: str) -> StorageService:
    if settings.environment == "development":
        return LocalStorageService(folder)
    return R2StorageService(folder)