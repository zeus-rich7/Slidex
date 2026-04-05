from __future__ import annotations

from app.dto import Base


class Template(Base):
    title: str
    description: str
    template_path: str
    images: list[str]
    slides_count: int
    ratio: str
    format: str
    file_size: str
    color_scheme: str
    tags: list[str]
    badge: str
    category: str
    label: str
