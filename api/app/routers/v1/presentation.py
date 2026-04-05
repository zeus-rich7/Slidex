from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.factory import get_db
from app.crud import PresentationCRUD
from app.models import Presentation
from fastapi.templating import Jinja2Templates


router = APIRouter()

class SaveContentRequest(BaseModel):
    presentation_id: int
    content: str
class SaveContentResponse(BaseModel):
    success: bool
    message: str

class SavePlansRequest(BaseModel):
    presentation_id: int
    plans: list

class SaveSettings(BaseModel):
    presentation_id: int
    title: str
    author: str
    recipient: str
    slides: int
    language: str


@router.post("/editor/save-content")
async def save_editor_content(
    payload: SaveContentRequest,
    db = Depends(get_db),
    request: Request = None
):
    await PresentationCRUD(Presentation).update(db, payload.presentation_id, {'reference_text': payload.content})


    return SaveContentResponse(
        success=True,
        message="Content saved",
    )

templates = Jinja2Templates(directory="static")

@router.get("/editor/{presentation_id}")
async def get_editor(presentation_id: int, request: Request, db: AsyncSession = Depends(get_db)):

    presentation = await PresentationCRUD(Presentation).get(db, presentation_id)

    return templates.TemplateResponse("editor.html", {
        "request": request,
        "logo": "SlideX",
        "reference_text": '' if not presentation.reference_text else presentation.reference_text
    })

@router.get("/plans/{presentation_id}")
async def get_plans(presentation_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    presentation = await PresentationCRUD(Presentation).get(db, presentation_id)
    return templates.TemplateResponse("plans.html", {
        "request": request,
        "logo": "SlideX",
        "plans": presentation.plans
    })


@router.post("/plans/save-plans")
async def save_plans(
    payload: SavePlansRequest,
    db = Depends(get_db),
    request: Request = None
):
    await PresentationCRUD(Presentation).update(db, payload.presentation_id, {'plans': {'plans': payload.plans}})

    return SaveContentResponse(
        success=True,
        message="Content saved",
    )


@router.get("/settings/{presentation_id}")
async def get_settings(presentation_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    presentation = await PresentationCRUD(Presentation).get(db, presentation_id)
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "logo": "SlideX",
        "title": presentation.title,
        "author": presentation.author if presentation.author else "",
        "recipient": presentation.recipient if presentation.recipient else "",
        "slide_count": presentation.slides_count if presentation.slides_count is not None else 1,
        "lang": presentation.lang,
        "price_per_slide": 10
    })

@router.post("/settings/save")
async def save_plans(
    payload: SaveSettings,
    db = Depends(get_db),
    request: Request = None
):
    await PresentationCRUD(Presentation).update(db, payload.presentation_id, {"title": payload.title, "author": payload.author, "recipient": payload.recipient, "slides_count": payload.slides, "lang": payload.language})

    return SaveContentResponse(
        success=True,
        message="Content saved"
    )

