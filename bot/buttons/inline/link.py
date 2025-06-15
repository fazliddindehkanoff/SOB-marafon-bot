from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_link_button(url: str, text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]]
    )
