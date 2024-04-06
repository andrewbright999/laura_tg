from aiogram import Router, F

from aiogram.types import Message
from flights import search_flights

router = Router()
router.message.filter(lambda message: message.message_thread_id == 563)


@router.message(F.text)
async def flight_message(message: Message):
    await message.answer("<code>Сейчас что-нибудь найду</code>😉🌎✈️", parse_mode="HTML")
    flights = await search_flights(message.text)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
    print(*flights)
    for flight in flights:
        await message.answer(flight)
