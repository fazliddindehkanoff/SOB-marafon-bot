from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.selectors import get_marathon_tarifs


async def get_tarif_buttons(
    marathon_id: int,
    language_code: str,
) -> InlineKeyboardMarkup:
    tarifs = await get_marathon_tarifs(marathon_id)
    buttons = [
        [
            InlineKeyboardButton(
                text=tarif.get(f"name_{language_code}", "No Name"),
                callback_data=f"tarif_{tarif['id']}",
            )
        ]
        for tarif in tarifs
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
