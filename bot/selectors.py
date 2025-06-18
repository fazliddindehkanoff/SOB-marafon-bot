from asgiref.sync import sync_to_async
from .models import (
    TelegramUser,
    FAQ,
    BotAdminContactSettings,
    Marathon,
    MarathonTarif,
)


async def get_user(chat_id: str) -> bool | dict:
    user = await sync_to_async(
        TelegramUser.objects.filter(telegram_id=chat_id).first,
    )()
    if user:
        return user

    return False


@sync_to_async
def get_faq_data():
    return list(FAQ.objects.all())


async def get_all_faq(language: str) -> str:
    faqs = await get_faq_data()  # fully evaluated queryset

    if not faqs:
        return "There are no FAQs available."

    result = ""
    for idx, faq in enumerate(faqs, 1):
        if language == "ru":
            result += f"{idx}. {faq.question_ru} -- {faq.answer_ru}\n"
        else:
            result += f"{idx}. {faq.question_uz} -- {faq.answer_uz}\n"
    return result


async def get_user_language(chat_id: str) -> str | None:
    user = await get_user(chat_id)
    if user and hasattr(user, "language"):
        return user.language
    return None


@sync_to_async
def get_admin_username():
    settings = BotAdminContactSettings.objects.last()
    if settings and hasattr(settings, "admin_username"):
        return settings.admin_username
    return None


@sync_to_async
def is_admin(username: str) -> bool:
    return BotAdminContactSettings.objects.filter(
        admin_username=username,
    ).exists()


@sync_to_async
def get_list_of_users(
    region_codes: list[str] | None = None, status: list[str] | None = None
) -> list[dict]:
    if region_codes:
        users = TelegramUser.objects.filter(region__in=region_codes)
    else:
        users = TelegramUser.objects.all()
    if status:
        if len(status) == 1 and status[0] == "paid":
            users = users.filter(is_subscribed=True)
        elif len(status) == 1 and status[0] == "unpaid":
            users = users.filter(is_subscribed=False)

    return list(users.values("telegram_id"))


@sync_to_async
def get_last_marathon() -> Marathon:
    return Marathon.objects.last()


@sync_to_async
def get_marathon_tarifs(marathon_id: int) -> list[dict]:
    marathon = Marathon.objects.filter(id=marathon_id).first()
    if marathon:
        return list(
            marathon.tarifs.values("id", "name_uz", "name_ru", "price"),
        )
    return []


@sync_to_async
def get_tarif(tarif_id: int) -> dict | None:
    tarif = MarathonTarif.objects.filter(id=tarif_id).first()
    if tarif:
        return {
            "id": tarif.id,
            "name_uz": tarif.name_uz,
            "name_ru": tarif.name_ru,
            "price": tarif.price,
            "description_uz": tarif.description_uz,
            "description_ru": tarif.description_ru,
        }
    return None


@sync_to_async
def get_chosen_tarif(tarif_id: str) -> dict | None:
    return MarathonTarif.objects.filter(id=tarif_id).first()


async def get_chosen_tarif_private_link(chat_id: str) -> dict | None:
    user = await get_user(chat_id)
    if user and user.chosen_tarif:
        return user.chosen_tarif.private_channel_link
    return None
