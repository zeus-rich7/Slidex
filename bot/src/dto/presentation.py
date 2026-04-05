from typing import Optional

from src.dto import Base

class Presentation(Base):
    user_id: int
    title: Optional[str]
    author: Optional[str]
    recipient: Optional[int]
    slides_count: Optional[int]
    template_id: Optional[int]
    json_data: Optional[dict]
    plans: Optional[list]
    reference_text: Optional[str]
    lang: Optional[str]
    is_completed: bool
