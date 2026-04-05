from typing import Optional

from sqlalchemy import update, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src import dto
from src.infrastructure.database.dao.rdb import BaseDAO
from src.infrastructure.database.models import Presentation


class PresentationDAO(BaseDAO[Presentation]):
    def __init__(self, session: AsyncSession):
        super().__init__(Presentation, session)

    async def add_presentation(self, user_id: int = None, title: str = None, author: str = None, template_id: int = None, json_data: dict = None,  reference_text: str = None, lang: str = None):
        presentation = Presentation(
            user_id=user_id,
            title=title,
            author=author,
            template_id=template_id,
            json_data=json_data,
            reference_text=reference_text,
            lang=lang
        )
        self.session.add(presentation)
        await self.session.commit()
        return dto.presentation.Presentation.model_validate(presentation)

    async def get_presentation_by_id(self, presentation_id: int) -> dto.Presentation | None:
        presentation = await self.session.execute(
            select(Presentation).where(Presentation.id == presentation_id)
        )
        presentation = presentation.scalar_one_or_none()
        return presentation

    async def update_presentation_by_id(
            self, presentation_id: int, **kwargs
    ) -> None:
        await self.session.execute(
            update(Presentation).where(Presentation.id == presentation_id).values(**kwargs)
        )
        await self.session.commit()
