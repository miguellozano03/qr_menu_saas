import uuid
import aiobotocore.session
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import InvalidFile, MissingFilename
from .base import StorageService
from .utils import check_size, validate_image_signature, validate_extension

CHUNK = 1024 * 64

class R2StorageService(StorageService):
    def __init__(self, folder: str) -> None:
        self.folder = folder
        self.bucket = settings.r2_bucket_name
        self.endpoint_url = settings.r2_endpoint_url 
        self.public_url = settings.r2_public_url

    async def upload(self, file: UploadFile) -> str:
        if not file.filename:
            raise MissingFilename("Missing filename")

        ext = validate_extension(file.filename)
        first_chunk = await file.read(1024)

        if not validate_image_signature(first_chunk):
            raise InvalidFile("Invalid image file")

        total = len(first_chunk)
        check_size(total)

        chunks = [first_chunk]
        while chunk := await file.read(CHUNK):
            total += len(chunk)
            check_size(total)
            chunks.append(chunk)

        body = b"".join(chunks)
        filename = f"{uuid.uuid4()}.{ext}"
        key = f"{self.folder}/{filename}"

        session = aiobotocore.session.get_session()
        async with session.create_client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name="auto",
        ) as client:
            await client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=f"image/{ext}",
            )

        return f"{self.public_url}/{key}"