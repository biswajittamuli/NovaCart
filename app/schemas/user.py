from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# ---------- Request Schemas ----------

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


# ---------- Response Schemas ----------

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str