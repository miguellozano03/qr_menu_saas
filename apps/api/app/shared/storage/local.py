import os
import uuid
import aiofiles
from fastapi import UploadFile
from app.core.exceptions import InvalidFile, MissingFilename
from .base import StorageService
from .local_setup import UPLOAD_DIR
from .utils import check_size, validate_image_signature, validate_extension

CHUNK = 1024 * 64

class LocalStorageService(StorageService):
    def __init__(self, folder: str) -> None:
        self.folder = folder
        self.upload_dir = os.path.join(UPLOAD_DIR, folder)
        os.makedirs(self.upload_dir, exist_ok=True)

    async def upload(self, file: UploadFile) -> str:
        if not file.filename:
            raise MissingFilename("Missing filename")

        ext = validate_extension(file.filename)

        first_chunk = await file.read(1024)

        if not validate_image_signature(first_chunk):
            raise InvalidFile("Invalid image file")

        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(self.upload_dir, filename)

        total = len(first_chunk)
        check_size(total)

        async with aiofiles.open(path, "wb") as f:
            try:
                await f.write(first_chunk)
                while chunk := await file.read(CHUNK):
                    total += len(chunk)
                    check_size(total)
                    await f.write(chunk)
            except Exception:
                os.remove(path)
                raise

        return f"http://localhost:8000/uploads/{self.folder}/{filename}"