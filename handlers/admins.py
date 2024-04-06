from aiogram import  Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class sendMessage(StatesGroup):
    get_mess = State()
    

router = Router()


@router.message(Command('laurasay'))
async def laura_message(message: Message, command: CommandObject):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status in ["administrator", "creator"]:
        await message.delete()  
        text = command.args
        await message.answer(text)

    
@router.message(Command('lauramess'))
async def laura_copy_message(message: Message, state: FSMContext):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status in ["administrator", "creator"]:
        await message.delete()  
        await state.set_state(sendMessage.get_mess)
        
@router.message(Command('Mid'))
async def laura_copy_message(message: Message):
    mid = str(message.message_id)
    await message.answer(mid)
    
@router.message(sendMessage.get_mess)
async def laura_copy_message(message:Message, state: FSMContext):
    await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id,)
    await message.delete()  
    await state.clear()
    