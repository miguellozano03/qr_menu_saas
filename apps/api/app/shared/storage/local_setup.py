import os

UPLOAD_DIR = "uploads"

def init_storage():
    os.makedirs(UPLOAD_DIR, exist_ok=True)