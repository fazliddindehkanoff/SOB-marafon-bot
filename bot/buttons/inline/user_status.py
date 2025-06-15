from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

STATUSES = ["paid", "unpaid"]


def get_status_filter_keyboard(selected_statuses: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    for status in STATUSES:
        text = "To‘lagan" if status == "paid" else "To‘lamagan"
        display_text = text + (" ✅" if status in selected_statuses else "")
        buttons.append(
            InlineKeyboardButton(
                text=display_text, callback_data=f"toggle_status:{status}"
            )
        )

    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    rows.append(
        [
            InlineKeyboardButton(
                text="✅ Barchasi", callback_data="all_statuses_selected"
            )
        ]
    )
    rows.append(
        [InlineKeyboardButton(text="➡️ Davom etish", callback_data="status_done")]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)
