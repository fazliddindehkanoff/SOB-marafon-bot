from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_payment_keyboard(language_code: str) -> InlineKeyboardMarkup:
    if language_code == "uz":
        back_text = "🔙 Ortga"
        pay_text = "💳 Toʻlov qilish"
    else:
        back_text = "🔙 Назад"
        pay_text = "💳 Оплатить"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=pay_text, pay=True)],
            [
                InlineKeyboardButton(
                    text=back_text,
                    callback_data="back_to_payment",
                ),
            ],
        ]
    )
