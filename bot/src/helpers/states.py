from aiogram.fsm.state import StatesGroup, State


class TermPaperForm(StatesGroup):
    theme = State()
    university = State()
    subject = State()

