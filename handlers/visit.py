from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

router = Router()

from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated, message: Message):
    await event.bot.delete_message(event.chat.id, message.message_id)

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated, message: Message):
    await event.bot.delete_message(event.chat.id, message.message_id)
