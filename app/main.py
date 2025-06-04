import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from asyncio import create_task

from app.routes.auth import router as auth_router
from app.routes.private import router as private_router
from app.routes.public import router as public_router
from app.database import create_tables
from app.repository import URLRepository

stop_background_task = False


async def deactivate_expired_urls_task():
    while not stop_background_task:
        count = await URLRepository.deactivate_expired_urls()
        print(f"[Фоновая задача] Деактивировано {count} просроченных ссылок")
        await asyncio.sleep(600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global stop_background_task

    await create_tables()
    print("БД готова к работе")

    task = create_task(deactivate_expired_urls_task())

    yield

    stop_background_task = True
    task.cancel()
    print("Выключение")

app = FastAPI(
    title="URL Alias Service",
    lifespan=lifespan
)

app.include_router(auth_router, tags=["Аутентификация"])
app.include_router(private_router, tags=["Приватные ручки"])
app.include_router(public_router, tags=["Переход по сокращенной ссылке"])
