import os

from app.core.exceptions import ImageExtensionNotAllowed, FileSizeNotAllowed

MAX_FILE_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 5 * 1024 * 1024))
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "svg"}

def validate_extension(filename: str):
    if not filename or not "." in filename:
        raise ImageExtensionNotAllowed("Missing file extension")
    
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        raise ImageExtensionNotAllowed("File extension not allowed. Only images are permitted.")
    return ext

def check_size(total: int):
    if total > MAX_FILE_SIZE:
        raise FileSizeNotAllowed("File too large")
    
def validate_image_signature(header: bytes) -> bool:
    header = header or b""

    if header.startswith(b"\x89PNG"):
        return True
    if header.startswith(b"\xff\xd8\xff"):
        return True
    if header.startswith(b"GIF8"):
        return True
    if header.startswith(b"RIFF") and b"WEBP" in header:
        return True
    if header.startswith(b"BM"):
        return True

    return False