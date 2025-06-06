from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.repository import UserRepository
from app.auth import access_security
from app import schemas

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user: Annotated[schemas.UserCreate, Depends()]) -> schemas.UserRead:
    existing_user = await UserRepository.get_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await UserRepository.create(user)


@router.post("/login")
async def login(user: Annotated[schemas.UserCreate, Depends()]) -> str:
    user_in_db = await UserRepository.get_by_credentials(user.username, user.password)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_security.create_access_token(subject={"id": user_in_db.id, "username": user_in_db.username})
