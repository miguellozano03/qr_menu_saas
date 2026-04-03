from abc import ABC, abstractmethod
from argon2 import PasswordHasher

class IPasswordService(ABC):

    @abstractmethod
    def hash(self, password_plain: str) -> str:
        pass
    
    @abstractmethod
    def verify(self, password_plain: str, hashed: str) -> bool:
        pass

class Argon2Hasher(IPasswordService):
    def __init__(self, hasher) -> None:
        self.__hasher = hasher

    def hash(self, password_plain: str) -> str:
        return self.__hasher.hash(password_plain)
    
    def verify(self, password_plain: str, stored_value: str) -> bool:
        try:
            return self.__hasher.verify(stored_value, password_plain)
        except Exception:
            return False

argon2_engine = PasswordHasher()
service = Argon2Hasher(argon2_engine)