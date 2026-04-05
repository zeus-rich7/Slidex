from sqlalchemy import ForeignKey, String, SmallInteger, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class Presentation(BaseModel):
    __tablename__ = "presentations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="presentations")

    title: Mapped[str] = mapped_column(String(255), nullable=True)
    author: Mapped[str] = mapped_column(String(50), nullable=True)
    recipient: Mapped[str] = mapped_column(String, nullable=True)
    slides_count: Mapped[int] = mapped_column(SmallInteger, nullable=True,  default=1)
    template_id: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    json_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    plans: Mapped[dict] = mapped_column(JSONB, nullable=True)
    reference_text: Mapped[str] = mapped_column(String(2000), nullable=True)
    lang: Mapped[str] = mapped_column(String(10), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
