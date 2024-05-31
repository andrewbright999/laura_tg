from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

router = Router() 
router.message.filter(lambda message: message.from_user.is_bot == False)

@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    await message.delete()

@router.chat_member.update(ChatMemberUpdatedFilter(IS_NOT_MEMBER))
async def handle_member_leave(event: ChatMemberUpdated):
    # Получаем сообщение, которое нужно удалить
    message = event.message
    if message:
        await message.bot.delete_message(message.chat.id, message.message_id)