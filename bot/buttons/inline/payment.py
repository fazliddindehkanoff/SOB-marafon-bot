from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_payment_keyboard(language_code: str) -> InlineKeyboardMarkup:
    if language_code == "uz":
        pay_text = "💳 Toʻlov qilish"
    else:
        pay_text = "💳 Оплатить"

    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=pay_text, pay=True)]]
    )
