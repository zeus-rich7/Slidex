from aiogram import Dispatcher

from .main_menu import router as main_menu_router
from .presentation_menu import router as presentation_menu_router
from .term_paper_menu import router as term_paper_router


def setup(dp: Dispatcher):
    dp.include_router(main_menu_router)
    dp.include_router(presentation_menu_router)
    dp.include_router(term_paper_router)
