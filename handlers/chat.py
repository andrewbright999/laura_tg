from aiogram import Router, F
from aiogram.types import Message
from profinity_filter.cens import check



faq_thread = 4 #Royal fish
# faq_thread = 163 #Test

router = Router()
router.message.filter(lambda message: message.message_thread_id == faq_thread)

@router.message(F.text)
async def message_chek(message: Message):
    check_result = await check(message.text)
    if check_result == "Мат":
        await message.answer("<b><i>Сообщение удалено из-за нецензурной лексики</i></b>")
        await message.delete()
    elif check_result == "Религия":
        message.answer("<b><i>Сообщение удалено из-за обсуждения религии или политики</i></b>")
        await message.delete()