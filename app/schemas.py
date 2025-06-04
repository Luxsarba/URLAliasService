from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime


# User

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


# URL

class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    expires_in_days: int = 1


class URLRead(BaseModel):
    id: int
    short_code: str
    original_url: HttpUrl
    is_active: bool
    created_at: datetime
    expires_at: datetime | None
    owner_id: int
    clicks: int

    class Config:
        from_attributes = True
