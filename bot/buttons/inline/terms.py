from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_terms_keyboard(lang):
    accept_text = "✅ Qabul qilaman" if lang == "uz" else "✅ Принимаю"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=accept_text,
                    callback_data="accept_terms",
                ),
            ]
        ]
    )
