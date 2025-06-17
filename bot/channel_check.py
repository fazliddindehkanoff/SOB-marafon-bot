# bot/middlewares/channel_check.py
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ChatMemberStatus

from bot.constants import Buttons

logger = logging.getLogger(__name__)
PUBLIC_CHANNEL_ID = -1001762497348


class ChannelJoinMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Only process Message and CallbackQuery events
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        # Skip if no user (shouldn't happen, but safety check)
        if not event.from_user:
            return await handler(event, data)

        if isinstance(event, Message):
            if event.text in [
                "/start",
                Buttons.uzbek_lang.value,
                Buttons.russian_lang.value,
            ]:
                print("Skipping channel check for start command or language selection")
                return await handler(event, data)

        user_id = event.from_user.id
        bot = data.get("bot")  # Get bot from data instead of event.bot

        try:
            member = await bot.get_chat_member(
                chat_id=PUBLIC_CHANNEL_ID, user_id=user_id
            )

            if member.status not in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR,
            ]:
                if isinstance(event, Message):
                    await event.answer(
                        "❗️ Botdan foydalanish uchun kanalga a'zo bo'lishingiz kerak: https://t.me/gayrats_blog"
                    )
                elif isinstance(event, CallbackQuery):
                    await event.message.answer(
                        "❗️ Botdan foydalanish uchun kanalga a'zo bo'lishingiz kerak: https://t.me/your_channel_username",
                    )
                return

        except TelegramBadRequest as e:
            logger.error(f"Failed to fetch chat member info for user {user_id}: {e}")

            # Handle error response based on event type
            if isinstance(event, Message):
                await event.answer(
                    f"Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.:{e}"
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
                    show_alert=True,
                )
            return

        except Exception as e:
            logger.error(f"Unexpected error in channel middleware: {e}")
            return await handler(
                event, data
            )  # Continue processing on unexpected errors

        # User is a member, continue with handler
        return await handler(event, data)
