from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime, UTC

from app.repository import URLRepository

router = APIRouter()


@router.get("/{short_code}")
async def redirect_to_original(short_code: str):
    url = await URLRepository.get_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    if not url.is_active:
        raise HTTPException(status_code=403, detail="Short URL is deactivated")

    now = datetime.now(UTC)
    if url.expires_at:
        expires_at = url.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at < now:
            raise HTTPException(status_code=410, detail="Short URL has expired")

    await URLRepository.increment_clicks(short_code)
    return RedirectResponse(str(url.original_url))
