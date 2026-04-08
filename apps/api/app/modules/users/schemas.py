from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not any(char.islower() for char in value):
            raise ValueError("Must have at least one lowercase letter.")
        if not any(char.isupper() for char in value):
            raise ValueError("Must have at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Must have at least one number letter.")

        return value
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str | None):
        if value is None:
            return value

        if not any(char.islower() for char in value):
            raise ValueError("Must have at least one lowercase letter.")
        if not any(char.isupper() for char in value):
            raise ValueError("Must have at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Must have at least one number letter.")

        return value
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"

class LoginData(BaseModel):
    email: EmailStr
    password: str