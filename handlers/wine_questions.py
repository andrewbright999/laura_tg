import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from LauraGpt.laura_gpt_wines import answer_to_question, get_text
from profinity_filter.cens import definity_chek


wine_thread = 235 #Royal fish Laura chat

router = Router()
router.message.filter(lambda message: message.message_thread_id == wine_thread)


@router.message(Command("start")) 
async def cmd_start(message: Message):
    print(message.message_thread_id)
    await message.answer(
        "Здравствуйте, здесь я могу вам ответить на вопросы об Аргентинском вине",
        reply_markup=ReplyKeyboardRemove())

@router.message(F.video_note)
async def on_video_note(message: Message):
    file_id = message.video_note.file_id
    file = await message.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path, f"{message.message_id}.mp3")
    text = await get_text(f"{message.message_id}.mp3")
    if (await definity_chek(text)) == "Да":
        await message.delete()
    else:
        await message.answer(f'{await answer_to_question(message.text)}', reply_markup=ReplyKeyboardRemove())
    try:
        os.remove (f"{message.message_id-2}.mp3")
    except:
        pass

@router.message(F.voice)
async def on_voice(message: Message):
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path, f"{message.message_id}.mp3")
    text = await get_text(f"{message.message_id}.mp3")
    if (await definity_chek(text)) == "Да":
        await message.delete()
    else:
        await message.answer(f'{await answer_to_question(text)}', reply_markup=ReplyKeyboardRemove())
    try:
        os.remove (f"{message.message_id-2}.mp3")
    except:
        pass


@router.message(F.text)
async def message_with_text(message: Message):
    if (await definity_chek(message.text)) == "Да":
        await message.delete()
    else:
        await message.answer(f'{await answer_to_question(message.text)}', reply_markup=ReplyKeyboardRemove())