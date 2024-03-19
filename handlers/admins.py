from aiogram import  Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject


router = Router()

@router.message(Command('laurasay'))
async def laura_message(message: Message, command: CommandObject):
    await message.delete()
    text = command.args
    await message.answer(text)