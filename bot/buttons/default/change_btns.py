from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.constants import Buttons


def get_change_buttons(language_code: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=Buttons.change_language.value.get(language_code),
                ),
                KeyboardButton(
                    text=Buttons.change_phone.value.get(language_code),
                ),
            ],
            [
                KeyboardButton(
                    text=Buttons.change_region.value.get(language_code),
                ),
            ],
            [
                KeyboardButton(
                    text=Buttons.back.value.get(language_code),
                ),
            ],
        ],
        resize_keyboard=True,
    )
