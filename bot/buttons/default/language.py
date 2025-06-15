from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.constants import Buttons


def get_language_options():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=Buttons.uzbek_lang.value),
                KeyboardButton(text=Buttons.russian_lang.value),
            ]
        ],
        resize_keyboard=True,
        row_width=1,
    )
    return keyboard
