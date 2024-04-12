from aiogram import  Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from moviepy.editor import *
from moviepy.video.fx.all import crop


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
        
@router.message(Command('mid'))
async def laura_copy_message(message: Message):
    mid = str(message.message_id)
    await message.answer(mid)
    
@router.message(sendMessage.get_mess)
async def laura_copy_message(message:Message, state: FSMContext):
    await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id,)
    await message.delete()  
    await state.clear()
    
        
@router.message(F.video)
async def laura_copy_message(message: Message):
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