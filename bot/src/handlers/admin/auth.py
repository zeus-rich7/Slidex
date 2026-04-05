from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.helpers.filters import AdminFilter


router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command("panel"), StateFilter("*"))
async def admin_auth(message: types.Message, state: FSMContext):
    await state.clear()

    welcome_text = (f"<b>Salom, {message.from_user.full_name}👋 \n\n"
                    f"Admin paneliga xush kelibsiz! </b>")

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="⚙️ Konfiglar")]
        ]
    )

    await message.answer(
        text=welcome_text,
        reply_markup=kb
    )

