from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB


def make_connection_string(db: DB) -> str:
    url = (
        f"postgresql+asyncpg://{db.USER}:{db.PASSWORD}"
        f"@{db.HOST}/{db.NAME}"
        f"?async_fallback=True"
    )
    return url

engine = create_async_engine(make_connection_string(DB()), echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session