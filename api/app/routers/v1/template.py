import os
import secrets
import shutil
import sys

from aiofiles import os as async_os

from fastapi import APIRouter, Depends, Query, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.factory import get_db
from app.crud import SlideTemplateCRUD
from app.models import SlideTemplate
from fastapi.templating import Jinja2Templates

router = APIRouter()


UPLOAD_DIR = "/app/templates"
BOT_ADDRESS = "https://e3dc-195-158-9-110.ngrok-free.app"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, secrets.token_hex(10)+'.'+file.filename.split(".")[1])

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"path": file_path}

@router.post("/")
async def add(
    title: str,
    description: str,
    template_path: str,
    slides_count: int,
    ratio: str,
    color_scheme: str,
    badge: str,
    category: str,
    tags: list[str] = Query(...),
    images: list[str] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    stat = await async_os.stat(template_path)
    file_size = f"{round(stat.st_size / 1024 ** 2, 1)} MB"

    file_format = template_path.split('.')[-1].upper()
    label = title.split()[0].upper()
    return await SlideTemplateCRUD(SlideTemplate).insert(
        db=db,
        title=title,
        description=description,
        template_path=template_path,
        images=images,
        slides_count=slides_count,
        ratio=ratio,
        label=label,
        file_format=file_format,
        file_size=file_size,
        color_scheme=color_scheme,
        tags=tags,
        badge=badge,
        category=category,
    )

templates = Jinja2Templates(directory="static")
@router.get("/")
async def get_templates(request: Request, db: AsyncSession = Depends(get_db)):

    slide_templates = await SlideTemplateCRUD(SlideTemplate).get_multi(db)
    return templates.TemplateResponse("templates.html", {
        "request": request,
        "logo": "SlideX",
        "bot_address": BOT_ADDRESS,
        "templates": slide_templates
    })