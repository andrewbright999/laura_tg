from os import listdir

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.for_questions import faq_keyboard
from LauraGpt.laura_gpt import answer_to_question
from commons import questions_list
from profinity_filter.cens import check


faq_thread = 3 #Royal fish
# faq_thread = 163 #Test
folder_dir = "tours-data\\tours\\chili\\"

router = Router()
router.message.filter(lambda message: message.message_thread_id == faq_thread)


@router.message(Command("start")) 
async def cmd_start(message: Message):
    if message.message_thread_id == faq_thread:
        print(message.message_thread_id)
        await message.answer(
            "Можете задавать мне вопросы)",
            reply_markup=faq_keyboard()
        )

@router.message(F.text.lower() == "Ближайшие туры".lower())
async def answer_yes(message: Message):
    album_builder = MediaGroupBuilder(
        caption="""Ближайший тур:
<b><i>Чили 🇨🇱</i> с 10 по 19 марта</b> 7850 USD
         
Скидка постоянным гостям 30% и 50% членам Royal Fishing Club

Если Вы хотите познакомиться с топовыми бизнесменами Казахстана и наладить связи для работы через Казахстан, то эта поездка для Вас!

Royal Fishing Club - это не только про рыбалку, это и про качественный нетворкинг, уникальные деловые связи, которые возникают благодаря общему хобби.

<a href="https://royal-safari.com/blog/best-tours/rfc_hot_tour_chili/">Программа тура</a>"""
    )
    for images in listdir(folder_dir):
        if (images.endswith(".jpg")):
            album_builder.add(type="photo",media=FSInputFile(f"{folder_dir}\\{images}"))
    await message.answer_media_group(
        # Не забудьте вызвать build()
        media=album_builder.build(),
        reply_markup=faq_keyboard(), 
        parse_mode="HTML"
    )

@router.message(F.text.lower() == "Уровни доступа".lower())
async def answer_no(message: Message):
    await message.answer(questions_list.q1.get_description(),reply_markup=faq_keyboard(),parse_mode="HTML")


@router.message(F.text)
async def message_with_text(message: Message):
    check_result = await check(message.text)
    if check_result == "Мат":
        await message.answer("<b><i>Сообщение удалено из-за нецензурной лексики</i></b>")
        await message.delete()
    elif check_result == "Религия":
        message.answer("<b><i>Сообщение удалено из-за обсуждения религии или политики</i></b>")
        await message.delete()
    else:
        answer = await answer_to_question(message.text)
        await message.answer(f'{answer}', reply_markup=faq_keyboard())
