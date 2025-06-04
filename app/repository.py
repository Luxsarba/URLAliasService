from app.database import async_session
from sqlalchemy import select, update

from datetime import datetime, timedelta, UTC
from pydantic import HttpUrl

from app import models, schemas


class UserRepository:
    @classmethod
    async def create(cls, user: schemas.UserCreate) -> schemas.UserRead:
        async with async_session() as session:
            user_dict = user.model_dump()
            new_user = models.User(**user_dict)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return schemas.UserRead.model_validate(new_user)

    @classmethod
    async def get_by_credentials(cls, username: str, password: str) -> schemas.UserRead | None:
        async with async_session() as session:
            stmt = select(models.User).where(
                models.User.username == username,
                models.User.password == password,
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            return schemas.UserRead.model_validate(user) if user else None

    @classmethod
    async def get_by_username(cls, username: str) -> schemas.UserRead | None:
        async with async_session() as session:
            stmt = select(models.User).where(models.User.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            return schemas.UserRead.model_validate(user) if user else None


class URLRepository:
    @classmethod
    async def create_short(cls, short_code: str,
                           original_url: HttpUrl,
                           owner_id: int,
                           expires_in_days: int = 1) -> schemas.URLRead:
        async with async_session() as session:
            expiration_date = datetime.now(UTC) + timedelta(days=expires_in_days)
            new_url = models.URL(
                short_code=short_code,
                original_url=str(original_url),
                is_active=True,
                created_at=datetime.now(UTC),
                expires_at=expiration_date,
                owner_id=owner_id,
            )
            session.add(new_url)
            await session.commit()
            await session.refresh(new_url)
            return schemas.URLRead.model_validate(new_url)

    @classmethod
    async def increment_clicks(cls, short_code: str) -> None:
        async with async_session() as session:
            stmt = (
                select(models.URL)
                .where(models.URL.short_code == short_code))
            result = await session.execute(stmt)
            url = result.scalar_one_or_none()
            if url:
                url.clicks += 1
                await session.commit()

    @classmethod
    async def deactivate_url(cls, code: str, owner_id: int) -> bool:
        async with async_session() as session:
            stmt = (
                update(models.URL)
                .where(models.URL.short_code == code,
                       models.URL.owner_id == owner_id)
                .values(is_active=False))
            await session.execute(stmt)
            await session.commit()
            return True

    @classmethod
    async def deactivate_expired_urls(cls) -> int:
        async with async_session() as session:
            now = datetime.now(UTC)
            stmt = (
                update(models.URL)
                .where(models.URL.is_active == True)
                .where(models.URL.expires_at < now)
                .values(is_active=False)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount

    @classmethod
    async def get_by_code(cls, code: str) -> schemas.URLRead | None:
        async with async_session() as session:
            stmt = select(models.URL).where(models.URL.short_code == code)
            result = await session.execute(stmt)
            url = result.scalar_one_or_none()
            return schemas.URLRead.model_validate(url) if url else None

    @classmethod
    async def get_user_urls(cls, owner_id: int, active_only: bool = False) -> list[schemas.URLRead]:
        async with async_session() as session:
            stmt = select(models.URL).where(models.URL.owner_id == owner_id)
            if active_only:
                stmt = stmt.where(models.URL.is_active)
            result = await session.execute(stmt)
            urls = list(result.scalars().all())
            return [schemas.URLRead.model_validate(url) for url in urls]

    @classmethod
    async def get_top_urls(cls, limit: int = 10, offset: int = 0) -> list[schemas.URLRead]:
        async with async_session() as session:
            stmt = (
                select(models.URL)
                .where(models.URL.is_active)
                .order_by(models.URL.clicks.desc())
                .offset(offset)
                .limit(limit))
            result = await session.execute(stmt)
            urls = list(result.scalars().all())
            return [schemas.URLRead.model_validate(url) for url in urls]
