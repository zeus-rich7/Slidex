from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.dao.rdb import BaseDAO, UserDAO, PresentationDAO, AdminDAO, ConfigDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.user = UserDAO(self.session)
        self.presentation = PresentationDAO(self.session)
        self.admin = AdminDAO(self.session)
        self.config = ConfigDAO(self.session)
