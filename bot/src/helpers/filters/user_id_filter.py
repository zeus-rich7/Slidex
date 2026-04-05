from abc import ABC, abstractmethod
from typing import List

from aiogram.filters import Filter
from aiogram.types import Message

from config import load_config
from src.infrastructure.database.dao import HolderDao
from src.infrastructure.database.factory import create_pool, make_connection_string


class AsyncUserIdFilter(Filter, ABC):

    @abstractmethod
    async def get_user_ids(self) -> List[int]:
        ...

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False

        allowed_ids = await self.get_user_ids()
        return message.from_user.id in allowed_ids


class AdminFilter(AsyncUserIdFilter):

    async def get_user_ids(self) -> List[int]:
        config = load_config()
        pool = create_pool(url=make_connection_string(config))
        async with pool() as session:
            holder = HolderDao(session=session)
            admins = await holder.admin.get_admins_list()
            return admins
