from aiogram import  Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from moviepy.editor import *
from moviepy.video.fx.all import crop


class sendMessage(StatesGroup):
    get_mess = State()
    
class sendRound(StatesGroup):
    get_round = State()

class sendSay(StatesGroup):
    start_mess = State()
    end_mess = State()

start_id = 0
end_id = 0
messages = []

router = Router()


@router.message(Command('mid'))
async def laura_get_message(message: Message):
    mid = str(message.message_id)
    await message.answer(mid)
    
@router.message(Command('chat_id'))
async def laura_message(message: Message, command: CommandObject):
    chat_id = message.chat.id
    await message.answer(chat_id)


@router.message(Command('laurasay'))
async def laura_message(message: Message, command: CommandObject):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status in ["administrator", "creator"]:
        await message.delete()  
        text = command.args
        await message.answer(text)


@router.message(Command('start_say'))
async def start_message(message: Message, state: FSMContext):
    global messages
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.delete()  
    messages = []
    await state.set_state(sendSay.start_mess)


@router.message(sendSay.start_mess, Command('end'))
async def end_message(message: Message, command: CommandObject, state: FSMContext):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if command.args:
        chat_id = (command.args).split("/")
        print(chat_id)
        await message.delete()  
        if len(chat_id)>1: 
            thread_id = chat_id[1]
            chat_id = chat_id[0]
            print(thread_id,chat_id)
            await message.bot.copy_messages(from_chat_id=message.chat.id, message_thread_id=thread_id, chat_id=chat_id, message_ids=messages)
            await message.bot.delete_messages(chat_id=message.chat.id, message_ids=messages)
            await state.clear()
        else: 
            chat_id = chat_id[0]
            print(chat_id)
            await message.bot.copy_messages(from_chat_id=message.chat.id, chat_id=chat_id, message_ids=messages)
            await message.bot.delete_messages(chat_id=message.chat.id, message_ids=messages)
            await state.clear()
    else:
        await message.bot.copy_messages(from_chat_id=message.chat.id, chat_id=message.chat.id, message_ids=messages)
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=messages)
        await state.clear()


@router.message(sendSay.start_mess)
async def append_message(message: Message, state: FSMContext):
    global messages
    messages.append(message.message_id)
    await state.set_state(sendSay.start_mess)
    # await message.delete()  
    
@router.message(Command('lauramess'))
async def laura_copy_message(message: Message, state: FSMContext):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status in ["administrator", "creator"]:
        await message.delete()  
        await state.set_state(sendMessage.get_mess)

    
# @router.message(sendMessage.get_mess)
# async def laura_copy_message(message:Message, state: FSMContext):
#     if message.text != "/end":
#         await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id,)
#         await message.delete()  
#         await state.clear()
#     else:
    
    
    
        
@router.message(Command('round'))
async def get_video(message: Message, state: FSMContext):
    await message.delete()  
    await state.set_state(sendRound.get_round)
        
        
        
@router.message(F.video, sendRound.get_round)
async def laura_copy_message(message: Message, state: FSMContext):
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (member.status in ["administrator", "creator"]) or (message.chat.id == 1263494893):
        # await message.delete()
        file_id = message.video.file_id
        file = await message.bot.get_file(file_id)
        await message.bot.download_file(file.file_path, "video.mov")
        await message.delete()
        clip = VideoFileClip("video.mov")
        clip_resized = clip.resize(width=299)
        cropped_clip = crop(clip_resized, x1 = 1, y1 = 1,  width = 399, height = 399)
        clip_resized = cropped_clip.resize(width=299)
        clip_resized.write_videofile("video1.mov",codec="libx264")
        video = FSInputFile("video1.mov", "rb")
        await message.answer_video_note(video_note=video)
        await state.clear()