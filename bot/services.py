from asgiref.sync import sync_to_async
from .models import TelegramUser


async def create_user(
    chat_id: str,
    phone_number: str,
    name: str,
    region: str,
    language_code: str,
) -> None:
    await sync_to_async(TelegramUser.objects.create)(
        telegram_id=chat_id,
        phone_number=phone_number,
        full_name=name,
        region=region,
        language=language_code,
    )


async def update_user(chat_id: str, **kwargs) -> None:
    allowed_fields = {"phone_number", "full_name", "region", "language"}
    update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
    if update_data:
        await sync_to_async(
            TelegramUser.objects.filter(telegram_id=chat_id).update,
        )(**update_data)
