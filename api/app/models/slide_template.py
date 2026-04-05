from sqlalchemy import SmallInteger, String, BigInteger, ARRAY, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models import BaseModel


class SlideTemplate(BaseModel):
    __tablename__ = "slide_templates"

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    template_path: Mapped[str] = mapped_column(String)
    images: Mapped[list] = mapped_column(ARRAY(Text))
    slides_count: Mapped[int] = mapped_column(SmallInteger)
    ratio: Mapped[str] = mapped_column(String(5))
    format: Mapped[str] = mapped_column(String(30))
    file_size: Mapped[str] = mapped_column(String(10))
    color_scheme: Mapped[str] = mapped_column(String, nullable=True)
    tags: Mapped[list] = mapped_column(ARRAY(Text), nullable=True)
    badge: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String)
    label: Mapped[str] = mapped_column(String)