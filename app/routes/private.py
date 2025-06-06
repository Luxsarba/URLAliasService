from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
import secrets

from app import schemas
from app.auth import login_required
from app.repository import URLRepository

router = APIRouter(prefix="/private")


@router.post("/shorten")
async def create_short_url(
        data: Annotated[schemas.URLCreate, Depends()],
        user: dict = Depends(login_required),
) -> schemas.URLRead:
    short_code = secrets.token_urlsafe(6)
    return await URLRepository.create_short(
        short_code=short_code,
        original_url=data.original_url,
        owner_id=user["id"],
        expires_in_days=data.expires_in_days or 1
    )


@router.get("/my")
async def get_my_urls(
        active_only: bool = False,
        user: dict = Depends(login_required),
) -> list[schemas.URLRead]:
    return await URLRepository.get_user_urls(user["id"], active_only)


@router.patch("/deactivate/{short_code}")
async def deactivate_url(
        short_code: str,
        user: dict = Depends(login_required),
):
    url = await URLRepository.get_by_code(short_code)
    if not url or url.owner_id != user["id"]:
        raise HTTPException(status_code=404, detail="URL not found")
    await URLRepository.deactivate_url(short_code, user["id"])
    return {"detail": f"Short URL {short_code} deactivated"}


@router.get("/stats")
async def get_top_urls(
    limit: int = 10,
    offset: int = 0,
    _user: dict = Depends(login_required),
) -> list[schemas.URLRead]:
    return await URLRepository.get_top_urls(limit=limit, offset=offset)
