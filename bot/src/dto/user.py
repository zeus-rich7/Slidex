from __future__ import annotations

from src.dto import Base


class User(Base):
    telegram_id: int
    balance: int
    referrals_count: int
