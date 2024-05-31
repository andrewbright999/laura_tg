from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

router = Router() 
router.message.filter(lambda message: message.from_user.is_bot == False)

@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    await message.delete()
    if len(message.new_chat_members)>1:
        user_names = []
        for user in message.new_chat_members:
            user_names.append(user.full_name)
            user_names = ", ".join(user.full_name)
    else:   
        user_names = message.new_chat_members[0].full_name
    await message.answer(f"""{user_names}, добро пожаловать в клуб <b>Royal Fishing Club</b>!

  Рады приветствовать вас в клубе, объединяющем людей, разделяющих страсть к рыбалке, природе и путешествиям. Здесь вы найдете много возможностей для активного отдыха и расширения своих бизнес-контактов.

  Теперь вы часть нашего клуба и мы готовы создавать незабываемые моменты, связанные с рыбной ловлей, приключениями и новыми дружбой.
                           
  Royal Fishing Club, здесь сбываются рыболовные мечты!""", parse_mode="HTML")

@router.chat_member.update(ChatMemberUpdatedFilter(IS_NOT_MEMBER))
async def handle_member_leave(event: ChatMemberUpdated):
    # Получаем сообщение, которое нужно удалить
    message = event.message
    if message:
        await message.bot.delete_message(message.chat.id, message.message_id)