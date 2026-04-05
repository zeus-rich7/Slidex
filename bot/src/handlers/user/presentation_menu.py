from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, InputFile, \
    FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from aiohttp import web

from src.helpers import Config
from src.infrastructure.database.dao import HolderDao
from src.services.presentation_manager import AIPresentation, Slide

router = Router()
routes = web.RouteTableDef()


class PresentationState(StatesGroup):
    title = State()
    author = State()
    design = State()
    confirmation = State()

@router.callback_query(F.data=="presentation_menu")
async def presentation_menu(call: CallbackQuery, state: FSMContext, dao: HolderDao):
    await state.set_state(PresentationState.title)
    await call.message.edit_text(
        text="""
        Taqdimot mavzusini kiriting:

💸 1 ta Slayd narxi(Nechta varaq bo'lishidan qatiy nazar): 5000 So'm

• Har bir mavzuga umumiy bilimdondek qarayman. Qaysidir tor doirada ishlatiladigan mavzularni kiritishda ularni mansubligi (guruh, oila, bo'lim) ko'rsatilsin. 
• Mavzuni batafsil yoritishga harakat qiling.
• Qisqartma so'zlarga, imloviy xatoli so'zlarga tushunmay qolishim mumkin.
• Quyidagilarga o'xshash mavzularni kiritishda davlat nomini ham qo'shib kiriting: 'Ona-Tili', 'Milliy-Musiqalar', 'Milliy O'yinlar'.
❗️ Kiritilgan mavzuga tushunmagan holda boshqa mavzuga chalg'ib ketishim mumkin. Iltimos, mavzu yozishda e'tiborli bo'ling.
        """
    )

@router.message(StateFilter(PresentationState.title))
async def get_title(msg: Message, dao: HolderDao, state: FSMContext):
    title = msg.text
    user = await dao.user.get_user_by_telegram_id(telegram_id=msg.chat.id)
    presentation = await dao.presentation.add_presentation(
        user_id=user.id,
        title=title
    )

    await state.update_data(
        presentation_id=presentation.id,
        title=title
    )
    await state.set_state(PresentationState.author)


    await msg.answer(f"✍️ <b>Taqdimot muallifini kiriting:</b>\n\n"
                     f"<i>Muallif ismi(familiyasi)ni kiriting. Buni keyinchalik taqdimotni tayyorlash oldidan 'sozlamalar' menyusi orqali o'zgartirishingiz ham mumkin.</i>")

@router.message(StateFilter(PresentationState.author))
async def get_author(msg: Message, dao: HolderDao, state: FSMContext):
    state_data = await state.get_data()
    title = state_data["title"]
    presentation_id = state_data["presentation_id"]

    await dao.presentation.update_presentation_by_id(
        presentation_id=presentation_id,
        author=msg.text
    )
    await msg.answer(
        text="\"Dizayn tanlash\" tugmasiga bosing va taqdimot dizaynini tanlang \n\n"
        f"📌 Mavzu: {title}\n\n"
        "Dizayn nima?\n"
        "- Dizayn bu — sizning slaydingiz tashqi ko'rinishi(shabloni)\n"
        "Qanday dizayn tanlayman?\n"
        "- Dizayn tanlash tugmasiga bosing va o'zingizga kerakli mavzuga mos bo'lgan dizaynning ustiga bosing. Hosil bo'lgan oynadan tanlash tugmasini bosing.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Dizayn tanlash", web_app=WebAppInfo(url=f"{Config.webapp_url}/templates/"))],
                [InlineKeyboardButton(text="🚫 Bekor q-sh", callback_data="back-to-main")]
            ],
        )
    )



@routes.get("/health")
async def health(request: web.Request):
    return web.json_response({"status": "ok"})


@routes.post("/webapp-data")
async def process_webapp_data(request: web.Request):
    bot: Bot = request.app['bot']
    dp: Dispatcher = request.app['dp']
    data = await request.json()
    init_data_str = data.get('_auth')


    if not init_data_str:
        return web.json_response({"ok": False, "error": "No initData"}, status=400)

    try:
        parsed: WebAppInitData = safe_parse_webapp_init_data(
            token=bot.token,
            init_data=init_data_str
        )
    except ValueError:
        return web.json_response({"ok": False, "error": "Invalid initData"}, status=403)

    user = parsed.user

    key = StorageKey(
        bot_id=bot.id,  # important in multi-bot setups
        chat_id=user.id,  # private chat → user_id
        user_id=user.id,
    )
    state = FSMContext(
        storage=dp.storage,
        key=key
    )
    state_data = await state.get_data()
    title = state_data["title"]
    presentation_id = state_data["presentation_id"]


    await state.set_state(PresentationState.confirmation)

    info_message = await bot.send_message(
        chat_id=user.id,
        text="Taqdimot haqida 👇\n\n"
             f"📌 Mavzu: {title}\n"
             "🏳️ Til: 🇺🇿 O'zbekcha\n"
             "👤 Muallif: b\n"
             "ℹ️ Ushbu malumotlar asosida taqdimotingiz tayyorlanadi. Agar nimadir maqul kelmagan bo'lsa yoki qandaydir xatolik bo'lsa sozlamalar menyusi orqali to'g'irlashingiz mumkin\n\n"
             "Foydali: Sizga berilgan darslik yoki adabiyotlar orqali qo'shimcha malumot kiritish sizga aniqroq, siz istagan slaydni olishda yordam beradi.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✍️ Malumotlarni tahrirlash", web_app=WebAppInfo(url=Config.webapp_url + f"/presentation/editor/{presentation_id}"))],
                [InlineKeyboardButton(text="➕ Reja qo'shish", web_app=WebAppInfo(url=Config.webapp_url + f"/presentation/plans/{presentation_id}"))],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", web_app=WebAppInfo(url=Config.webapp_url + f"/presentation/settings/{presentation_id}"))],
                [InlineKeyboardButton(text="✅ Davom etish", callback_data=f"construct-presentation")],
                [InlineKeyboardButton(text="🚫 Bekor q-sh", callback_data="back-to-main")],
            ]
        )
    )
    await bot.delete_message(
        chat_id=user.id,
        message_id=info_message.message_id-1,
    )

    return web.json_response({
        "ok": True,
        "user_id": user.id,
        "first_name": user.first_name,
        "username": user.username,
        "message": "Data validated successfully!"
    })

@router.callback_query(F.data == "construct-presentation")
async def construct_presentation(call: CallbackQuery, state: FSMContext, dao: HolderDao):
    state_data = await state.get_data()
    presentation_id = state_data["presentation_id"]
    await state.clear()

    presentation = await dao.presentation.get_presentation_by_id(presentation_id)


    notification = await call.message.edit_text(
        "<b>Suniy intellektga so'rov jo'natilmoqda..</b>"
    )
    note_emoji = await call.message.answer("📝")

    presentation_ai = AIPresentation(
        topic=presentation.title,
        chars_per_content=800,
        lang=presentation.lang
    )
    json_presentation = await presentation_ai.get_json_data()
    while not json_presentation["success"]:
        json_presentation = await presentation_ai.get_json_data()

    await notification.edit_text(
        "<b>Suniy intellektdan javob qabul qilindi. Natija yozilmoqda...</b>"
    )
    destination = f"./files/temp/{call.message.message_id}.pptx"
    slide = Slide(
        output_path=destination,
        title=presentation.title,
        author=presentation.author,
        recipient="presentation.recipient",
        template_path="/app/templates/eda9e05a069ee0bbe855.pptx",
        json_data=json_presentation["data"],
    )
    await slide.construct()
    await slide.save()

    await note_emoji.delete()
    await notification.delete()

    await call.message.answer_document(
        document=FSInputFile(path=destination)
    )

