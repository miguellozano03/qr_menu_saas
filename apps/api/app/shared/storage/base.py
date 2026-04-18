from abc import ABC, abstractmethod
from fastapi import UploadFile

class StorageService(ABC):
    
    @abstractmethod
    async def upload(self, file: UploadFile) -> str:
        pass