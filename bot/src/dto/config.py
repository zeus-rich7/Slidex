from __future__ import annotations

from src.dto import Base


class Config(Base):
    key: str
    value: str
