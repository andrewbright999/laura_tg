from aiogram.types import ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def faq_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ближайшие туры")
    kb.button(text="Уровни доступа")
    kb.button(text="Корпоративное партнерство")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
