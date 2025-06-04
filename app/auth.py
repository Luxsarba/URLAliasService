import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")

access_security = JwtAccessBearer(secret_key=SECRET_KEY)


def get_current_user(credentials: JwtAuthorizationCredentials = Security(access_security)) -> dict:
    return credentials.subject


def login_required(user: dict = Depends(get_current_user)) -> dict:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
