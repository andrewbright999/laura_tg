from aiogram import  Router, F
from aiogram.types import Message
from keyboards.for_questions import faq_keyboard

router = Router()
router.message.filter()



@router.message(F.text.startswith('Лаура: '))
async def laura_message(message: Message):
    await message.delete()
    await message.answer(message.text.removeprefix('Лаура: '))