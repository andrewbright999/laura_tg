from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

router = Router() 
router.message.filter(lambda message: message.from_user.is_bot == False)

@router.chat_member()
async def on_chat_member_updated(event: ChatMemberUpdated):
    if event.new_chat_member.status in [types.ChatMemberStatus.LEFT, types.ChatMemberStatus.KICKED]:
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.from_user.id)
    elif event.new_chat_member.status == types.ChatMemberStatus.MEMBER:
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.from_user.id)