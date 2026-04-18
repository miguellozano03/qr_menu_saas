from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import AppException

def register_exceptions_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def global_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )
        
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        orig = str(exc.orig)

        if "foreign key" in orig.lower():
            message = "One or more referenced resources do not exist"
        elif "unique" in orig.lower():
            message = "Resource already exists"
        elif "not null" in orig.lower():
            message = "Missing required fields"
        else:
            message = "Database constraint violation"
        
        return JSONResponse(
            status_code=409,
            content={"error": message}
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )