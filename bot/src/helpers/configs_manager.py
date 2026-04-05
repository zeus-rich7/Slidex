from dataclasses import dataclass, fields

from config import load_config
from src.infrastructure.database.dao import HolderDao
from src.infrastructure.database.factory import create_pool, make_connection_string



@dataclass
class Config:
    """
    Just create an attribute and it will be saved to DB and cached.
    You can use it in your code, without hassle or extra load the DB
    """
    admin_id: int = 1
    webapp_url: str = "https://vphrd-195-158-9-110.a.free.pinggy.link"

    async def initialize(self):
        db_config = load_config()
        pool = create_pool(make_connection_string(db_config))
        async with pool() as session:
            holder = HolderDao(session=session)
            for field in fields(self.__class__):
                if field.default is None:
                    value = None
                else:
                    value = str(field.default)

                key = field.name
                config = await holder.config.get_config_by_key(key)
                if not config:
                    await holder.config.add_config(key=key, value=value)

    @classmethod
    async def refresh(cls):
        db_config = load_config()
        pool = create_pool(make_connection_string(db_config))
        async with pool() as session:
            holder = HolderDao(session=session)
            configs = await holder.config.get_configs_list()
            for config in configs:
                setattr(cls, config.key, config.value)

    @classmethod
    async def type_validate(cls):
        for field in fields(cls):
            db_config = load_config()
            pool = create_pool(make_connection_string(db_config))
            async with pool() as session:
                holder = HolderDao(session=session)
                config = await holder.config.get_config_by_key(field.name)
                value = config.value
                if field.type is bool:
                    value = value[0].lower() in ['y', 't', 'true', 'yes', 'on']
                elif field.type is int:
                    value = int(value)
                setattr(cls, field.name, value)

