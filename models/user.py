from pydantic import BaseModel, Field
from datetime import datetime


class UserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    is_active: bool
    status: str
    avatar_url: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool
    is_admin: bool = Field(default=False)
    status: str
    avatar_url: str
    created_at: datetime
    last_seen: datetime

    class Config:
        orm_mode = True
