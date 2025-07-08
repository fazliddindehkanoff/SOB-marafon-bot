from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.constants import Buttons


def get_main_menu_keyboards(language_code: str = "uz"):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=Buttons.faq.value.get(language_code),
                ),
                KeyboardButton(
                    text=Buttons.contact.value.get(language_code),
                ),
            ],
            [
                KeyboardButton(
                    text=Buttons.settings.value.get(language_code),
                ),
                KeyboardButton(
                    text=Buttons.tariffs.value.get(language_code),
                ),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
