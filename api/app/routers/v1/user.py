from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.factory import get_db
from app.crud import UserCRUD
from app.models import User


router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserCRUD(User).get(db, user_id)