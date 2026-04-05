from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models import BaseModel


class Admin(BaseModel):

    __tablename__ = "admin"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
