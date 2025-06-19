from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.constants import Buttons


def get_link_buttons(data: dict, language_code: str) -> InlineKeyboardMarkup:
    group_link = data["group"]
    channel_link = data["channel"]
    keyboards = [
        [
            InlineKeyboardButton(
                text=Buttons.join_channel.value.get(language_code),
                url=channel_link,
            )
        ]
    ]
    if group_link:
        keyboards.append(
            [
                InlineKeyboardButton(
                    text=Buttons.join_group.value.get(language_code),
                    url=group_link,
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboards)
