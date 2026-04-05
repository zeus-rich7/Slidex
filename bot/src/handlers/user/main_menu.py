from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.infrastructure.database.dao import HolderDao
from src.services.presentation_manager import AIPresentation

router = Router()


@router.message(CommandStart())
async def on_cmd_start(message: types.Message, dao: HolderDao):

    user = await dao.user.get_user_by_telegram_id(
        telegram_id=message.chat.id
    )
    if not user:
        await dao.user.add_user(telegram_id=message.chat.id)

    await message.answer(
        text=f"📚 <b>SlideX</b> – Siz uchun hammasini tayyorlaydi\n\n"
             f"🚀 <i>Sizning kundalik ishlaringizni bajarishingiz uchun yordamchi</i>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗞 Taqdimot", callback_data="presentation_menu"),
                 InlineKeyboardButton(text="📄 Referat", callback_data="term_paper_menu"),
                InlineKeyboardButton(text="✍️ Mustaqil ish", callback_data="independent_work_menu")],
            ]
        )
    )

@router.callback_query(F.data == "back-to-main", StateFilter("*"))
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=f"📚 <b>SlideX</b> – Siz uchun hammasini tayyorlaydi\n\n"
             f"🚀 <i>Sizning kundalik ishlaringizni bajarishingiz uchun yordamchi</i>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗞 Taqdimot", callback_data="presentation_menu"),
                 InlineKeyboardButton(text="📄 Referat", callback_data="term_paper_menu"),
                InlineKeyboardButton(text="✍️ Mustaqil ish", callback_data="independent_work_menu")],
            ]
        )
    )