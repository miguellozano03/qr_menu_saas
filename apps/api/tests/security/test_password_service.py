import pytest
from argon2 import PasswordHasher
from app.core.security.password_service import Argon2Hasher


@pytest.fixture(scope='module')
def hasher_service():
    engine = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
    return Argon2Hasher(engine)

def test_and_verify_sucess(hasher_service):
    raw_password: str = 'sample_password'

    hashed_password: str = hasher_service.hash(password_plain=raw_password)
    is_valid: bool = hasher_service.verify(raw_password, hashed_password)

    assert hashed_password != raw_password
    assert is_valid is True

def test_and_verify_fails_with_wrong_password(hasher_service):
    raw_password: str = 'correct_password'
    wrong_password: str = 'incorrect_password'

    hashed_password: str = hasher_service.hash(raw_password)
    is_valid: bool = hasher_service.verify(wrong_password, hashed_password)

    assert is_valid is False