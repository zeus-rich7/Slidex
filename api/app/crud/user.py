from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import BaseCRUD
from app.models import User

class UserCRUD(BaseCRUD[User]):
    async def get_by_telegram_id(self, db: AsyncSession, telegram_id: int) -> User | None:
        result = await db.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()


