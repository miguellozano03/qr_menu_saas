
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class IsDuplicatedException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 409)

class UnauthorizedException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, 401)

class ResourceNotFoundException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, 404)
        
class ImageExtensionNotAllowed(AppException):
    def __init__(self, message: str):
        super().__init__(message)
        
class FileSizeNotAllowed(AppException):
    def __init__(self, message: str):
        super().__init__(message, 413)
        
class InvalidFile(AppException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, 422)
        
class MissingFilename(AppException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)