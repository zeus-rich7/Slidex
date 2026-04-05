from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import BaseCRUD
from app.models import SlideTemplate


class SlideTemplateCRUD(BaseCRUD[SlideTemplate]):
    async def insert(
            self,
            db: AsyncSession,
            title: str,
            description: str,
            template_path: str,
            images: list[str],
            slides_count: int,
            ratio: str,
            label: str,
            file_format: str,
            file_size: str,
            color_scheme: str,
            tags: list[str],
            badge: str,
            category: str,
    ) -> SlideTemplate:
        obj = SlideTemplate(
            title=title,
            description=description,
            template_path=template_path,
            images=images,
            slides_count=slides_count,
            ratio=ratio,
            label=label,
            format=file_format,
            file_size=file_size,
            color_scheme=color_scheme,
            tags=tags,
            badge=badge,
            category=category,
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj