import os
from aiogram import Router, F
from aiogram.types import Message
from profinity_filter.cens import check, definity_chek
from LauraGpt.laura_gpt import get_text

faq_thread = 4 #Royal fish

router = Router()
router.message.filter(lambda message: message.message_thread_id == faq_thread)

@router.message(F.text)
async def message_chek(message: Message):
    check_result = await check(message.text)
    if check_result == "Мат":
        await message.answer("<b><i>Сообщение удалено из-за нецензурной лексики</i></b>")
        await message.delete()
    elif check_result == "Религия":
        message.answer("<b><i>Сообщение удалено из-за обсуждения религии или политики</i></b>")
        await message.delete()
    

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
        await message.reply(f'{text}')
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
        await message.reply(f'{text}')
    try:
        os.remove (f"{message.message_id-2}.mp3")
    except:
        pass
