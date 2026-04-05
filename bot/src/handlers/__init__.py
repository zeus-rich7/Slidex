from aiogram import Dispatcher

from src.handlers import user
from src.handlers import admin


def setup(dp: Dispatcher):
    user.setup(dp)
    admin.setup(dp)
