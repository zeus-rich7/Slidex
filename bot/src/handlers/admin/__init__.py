from aiogram import Dispatcher

from .auth import router as admin_auth
from .config_management import router as configs


def setup(dp: Dispatcher):
    dp.include_router(admin_auth)
    dp.include_router(configs)