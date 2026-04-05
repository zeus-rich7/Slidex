from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.helpers.states import TermPaperForm
from src.services.term_paper_manager import TermPaper, AITermPaper

router = Router()

@router.callback_query(F.data == "term_paper_menu")
async def term_paper_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="<b>Referat mavzusini jo'nating</b>"
    )
    await state.set_state(TermPaperForm.theme)

@router.message(TermPaperForm.theme)
async def theme_handler(message: Message, state: FSMContext):
    await state.set_state(TermPaperForm.subject)
    await state.update_data(
        theme=message.text
    )
    await message.answer(
        text="<b>Fan nomini jo'nating</b>"
    )

@router.message(TermPaperForm.subject)
async def subject_handler(message: Message, state: FSMContext):
    await state.set_state(TermPaperForm.university)
    await state.update_data(
        subject=message.text
    )
    await message.answer(
        text="<b>Universitet nomini jo'nating</b>"
    )

@router.message(TermPaperForm.university)
async def university_handler(message: Message, state: FSMContext):
    await state.set_state(TermPaperForm.university)
    state_data = await state.get_data()
    theme = state_data["theme"]
    subject = state_data["subject"]
    university = message.text

    ai = AITermPaper(topic=theme)
    json_content = await ai.get_json_data()
    destination = f"./files/temp/{message.message_id}.docx"
    term_paper = TermPaper(
        university=university,
        theme=theme,
        subject=subject,
        json_content=json_content["data"],
        output_path=destination
    )
    await term_paper.fill()
    await term_paper.save()

    await message.answer_document(
        document=FSInputFile(path=destination)
    )





