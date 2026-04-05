from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message

from src.handlers.admin.auth import admin_auth
from src.helpers import Config
from src.helpers.filters import AdminFilter

from src.infrastructure.database.dao import HolderDao

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


class ConfigStates(StatesGroup):
    get_key = State()
    get_value = State()



@router.message(F.text == "⚙️ Konfiglar", StateFilter("*"))
async def manage_configs(message: types.Message, state: FSMContext, dao: HolderDao):
    await state.set_state(ConfigStates.get_key)

    configs = await dao.config.get_configs_list()
    if configs:
        text = "<b>👇 Tahrirlash uchun sozlamani tanlang</b>"
    else:
        text = "<b>🤷‍♂️ Sizda xali sozlamalar mavjud emas</b>"

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=
        [
            [KeyboardButton(text=config.key)] for config in configs
        ]
    )

    await message.reply(
        text=text,
        reply_markup=kb
    )


@router.message(StateFilter(ConfigStates.get_key))
async def get_key(msg: Message, state: FSMContext, dao: HolderDao):
    key = msg.text

    await state.update_data(key=key)
    await state.set_state(ConfigStates.get_value)
    config = await dao.config.get_config_by_key(key)

    text = (f"🔑 Kalit: {config.key}\n"
            f"*️⃣ Qiymat: {config.value}\n\n"
            f"👇 Yangi qiymatni kiriting")

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🚫 Bekor qilish")
            ]
        ]
    )

    await msg.reply(
        text=text,
        reply_markup=markup
    )

@router.message(StateFilter(ConfigStates.get_value))
async def get_value(msg: Message, state: FSMContext, dao: HolderDao):
    state_data = await state.get_data()
    key = state_data["key"]
    value = msg.text

    await dao.config.update_config(key=key, value=value)
    await Config.refresh()
    await Config.type_validate()

    text = "🔄 Qiymat yangilandi"
    await msg.reply(text=text)

    await admin_auth(message=msg, state=state)
