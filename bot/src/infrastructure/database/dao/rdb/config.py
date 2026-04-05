from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import dto
from src.infrastructure.database.dao.rdb import BaseDAO
from src.infrastructure.database.models import Config


class ConfigDAO(BaseDAO[Config]):
    def __init__(self, session: AsyncSession):
        super().__init__(Config, session)

    async def add_config(
        self, key: str, value: str
    ) -> dto.Config:
        config = Config(key=key, value=value)
        self.session.add(config)
        await self.session.commit()
        return dto.Config.model_validate(config)

    async def get_config_by_key(
            self, key: str
    ) -> dto.Config | None:
        result = await self.session.execute(
            select(Config)
            .where(Config.key == key)
        )
        config = result.scalar()
        if config is not None:
            return dto.Config.model_validate(config)
        return None

    async def get_configs_list(self) -> List[dto.Config]:
        results = await self.session.execute(
            select(Config)
        )
        return  [dto.Config.model_validate(config) for config in results.scalars().all()]

    async def update_config(
            self, key: str, value: str
    ) -> dto.Config | None:
        config = await self.session.execute(
            update(Config).where(Config.key == key).values(value=value).returning(Config)
        )
        await self.session.commit()
        config = config.scalar()
        return config

