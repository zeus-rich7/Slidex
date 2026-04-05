from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import dto
from src.infrastructure.database.dao.rdb import BaseDAO
from src.infrastructure.database.models import Admin


class AdminDAO(BaseDAO[Admin]):
    def __init__(self, session: AsyncSession):
        super().__init__(Admin, session)

    async def add_admin(
        self, telegram_id: int
    ) -> dto.Admin:
        admin = Admin(telegram_id=telegram_id)
        self.session.add(admin)
        await self.session.commit()
        return dto.Admin.model_validate(admin)

    async def get_admin_by_telegram_id(
            self, telegram_id: int
    ) -> dto.Admin | None:
        result = await self.session.execute(
            select(Admin)
            .where(Admin.telegram_id == telegram_id)
        )
        user = result.scalar()
        if user is not None:
            return dto.Admin.model_validate(user)
        return None

    async def get_admins_list(self) -> List[int]:
        results = await self.session.execute(
            select(Admin)
        )
        return  [admin.telegram_id for admin in results.scalars().all()]
