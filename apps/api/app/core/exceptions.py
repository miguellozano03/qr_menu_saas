
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