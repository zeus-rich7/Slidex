from typing import List

from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models import BaseModel


class User(BaseModel):

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    balance: Mapped[int] = mapped_column(BigInteger, default=0)
    referrals_count: Mapped[int] = mapped_column(Integer, default=0)
    presentations: Mapped[List["Presentation"]] = relationship(back_populates="user")
