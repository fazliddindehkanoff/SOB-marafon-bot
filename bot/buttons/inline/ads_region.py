from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants import REGIONS


def get_region_filter_keyboard(
    selected_region_codes: list[str],
) -> InlineKeyboardMarkup:
    buttons = []
    for code, name in REGIONS:
        display_text = name + (" ✅" if code in selected_region_codes else "")
        buttons.append(
            InlineKeyboardButton(
                text=display_text, callback_data=f"toggle_region:{code}"
            )
        )

    # Chunk into rows (e.g., 2 per row)
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    # Add a done button
    rows.append(
        [
            InlineKeyboardButton(
                text="✅ Barchasi", callback_data="all_regions_selected"
            )
        ],
    )
    rows.append(
        [InlineKeyboardButton(text="➡️ Davom etish", callback_data="regions_done")]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)
