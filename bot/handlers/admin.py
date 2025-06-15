from aiogram import Router, types, F, Bot
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
import asyncio
import logging

from bot.states import AdminAdStates
from bot.selectors import is_admin
from bot.buttons import get_region_filter_keyboard, get_status_filter_keyboard
from bot.constants import REGIONS
from bot.selectors import get_list_of_users

admin_router = Router()

# Store media groups temporarily
media_groups = {}

logger = logging.getLogger(__name__)


def get_confirmation_keyboard():
    """Create confirmation keyboard with buttons"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha", callback_data="confirm_send_yes"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_send_no"),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Qayta yozish", callback_data="confirm_send_rewrite"
                ),
                InlineKeyboardButton(text="⬅️ Ortga", callback_data="confirm_send_back"),
            ],
        ]
    )
    return keyboard


async def send_advertisement_preview(
    message: Message, media: list, ad_text: str, is_media_group: bool = False
):
    """Send advertisement preview to admin"""
    if media:
        if len(media) == 1 and not is_media_group:
            # Single media item
            m = media[0]
            caption = ad_text or ""

            if m.photo:
                await message.answer_photo(m.photo[-1].file_id, caption=caption)
            elif m.video:
                await message.answer_video(m.video.file_id, caption=caption)
            elif m.document:
                await message.answer_document(m.document.file_id, caption=caption)
            elif m.audio:
                await message.answer_audio(m.audio.file_id, caption=caption)
            elif m.voice:
                await message.answer_voice(m.voice.file_id, caption=caption)
            elif m.video_note:
                await message.answer_video_note(m.video_note.file_id)
                if caption:
                    await message.answer(caption)
            elif m.animation:
                await message.answer_animation(m.animation.file_id, caption=caption)
            elif m.text:
                await message.answer(m.text)
        else:
            # Media group
            group = MediaGroupBuilder()
            for i, m in enumerate(media):
                caption = m.caption or ("" if i > 0 else ad_text or "")

                if m.photo:
                    group.add_photo(media=m.photo[-1].file_id, caption=caption)
                elif m.video:
                    group.add_video(media=m.video.file_id, caption=caption)
                elif m.document:
                    group.add_document(media=m.document.file_id, caption=caption)
                elif m.audio:
                    group.add_audio(media=m.audio.file_id, caption=caption)

            try:
                await message.answer_media_group(group.build())
            except Exception as e:
                await message.answer(f"Xatolik: Media group ko'rsatilmadi - {str(e)}")
    else:
        # Text only
        text = ad_text or ""
        if text:
            await message.answer(text)
        else:
            await message.answer("Bo'sh reklama")

    # Send confirmation message with buttons
    await message.answer(
        "Reklama qabul qilindi. Yuborishni xohlaysizmi?",
        reply_markup=get_confirmation_keyboard(),
    )


async def send_ad_to_user(
    bot: Bot, user_id: int, media: list, ad_text: str, is_media_group: bool
):
    """Send advertisement to a single user"""
    try:
        if media:
            if len(media) == 1 and not is_media_group:
                # Single media item
                m = media[0]
                caption = ad_text or ""

                if m.photo:
                    await bot.send_photo(user_id, m.photo[-1].file_id, caption=caption)
                elif m.video:
                    await bot.send_video(user_id, m.video.file_id, caption=caption)
                elif m.document:
                    await bot.send_document(
                        user_id, m.document.file_id, caption=caption
                    )
                elif m.audio:
                    await bot.send_audio(user_id, m.audio.file_id, caption=caption)
                elif m.voice:
                    await bot.send_voice(user_id, m.voice.file_id, caption=caption)
                elif m.video_note:
                    await bot.send_video_note(user_id, m.video_note.file_id)
                    if caption:
                        await bot.send_message(user_id, caption)
                elif m.animation:
                    await bot.send_animation(
                        user_id, m.animation.file_id, caption=caption
                    )
                elif m.text:
                    await bot.send_message(user_id, m.text)
            else:
                # Media group
                group = MediaGroupBuilder()
                for i, m in enumerate(media):
                    caption = m.caption or ("" if i > 0 else ad_text or "")

                    if m.photo:
                        group.add_photo(media=m.photo[-1].file_id, caption=caption)
                    elif m.video:
                        group.add_video(media=m.video.file_id, caption=caption)
                    elif m.document:
                        group.add_document(media=m.document.file_id, caption=caption)
                    elif m.audio:
                        group.add_audio(media=m.audio.file_id, caption=caption)

                await bot.send_media_group(user_id, group.build())
        else:
            # Text only
            text = ad_text or "Reklama"
            await bot.send_message(user_id, text)

        return True
    except TelegramForbiddenError:
        logger.warning(f"User {user_id} blocked the bot")
        return False
    except TelegramBadRequest as e:
        logger.error(f"Bad request for user {user_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending to user {user_id}: {e}")
        return False


@admin_router.message(F.text == "/send_advertisement")
async def send_advertisement(message: types.Message, state: FSMContext):
    if not message.from_user.username:
        await message.answer("Botdan foydalanish uchun username qo'shing.")
        return

    if not await is_admin(message.from_user.username):
        await message.answer("Sizga bu buyruqni ishlatishga ruxsat yo'q.")
        return

    await state.set_data(
        {
            "selected_regions": [],
            "admin_id": message.from_user.id,
            "all_regions": False,
            "all_statuses": False,
            "selected_statuses": [],
            "ad_text": "",
            "media": [],
            "is_media_group": False,
        }
    )

    await message.answer(
        "Reklama yuborish uchun regionlarni tanlang:",
        reply_markup=get_region_filter_keyboard([]),
    )
    await state.set_state(AdminAdStates.SELECT_REGIONS)


@admin_router.callback_query(
    AdminAdStates.SELECT_REGIONS, F.data.startswith("toggle_region:")
)
async def toggle_region(call: CallbackQuery, state: FSMContext):
    region = call.data.split(":")[1]
    data = await state.get_data()
    selected = data.get("selected_regions", [])

    if region in selected:
        selected.remove(region)
    else:
        selected.append(region)

    await state.update_data(selected_regions=selected, all_regions=False)
    await call.message.edit_reply_markup(
        reply_markup=get_region_filter_keyboard(selected)
    )
    await call.answer()


@admin_router.callback_query(
    AdminAdStates.SELECT_REGIONS, F.data == "all_regions_selected"
)
async def all_regions_selected(call: CallbackQuery, state: FSMContext):
    await state.update_data(all_regions=True, selected_regions=[])
    await call.message.answer("Tanlangan hududlar: Barchasi")
    await call.message.answer(
        "Foydalanuvchilar holatini tanlang:",
        reply_markup=get_status_filter_keyboard([]),
    )
    await state.set_state(AdminAdStates.SELECT_STATUS)
    await call.answer()


@admin_router.callback_query(AdminAdStates.SELECT_REGIONS, F.data == "regions_done")
async def regions_done_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_regions", [])
    if not selected:
        await call.answer("Iltimos, kamida bitta hudud tanlang.", show_alert=True)
        return

    region_names = [name for code, name in REGIONS if code in selected]
    await call.message.answer(f"Tanlangan hududlar: {', '.join(region_names)}")
    await call.message.answer(
        "Foydalanuvchilar holatini tanlang:",
        reply_markup=get_status_filter_keyboard([]),
    )
    await state.set_state(AdminAdStates.SELECT_STATUS)
    await call.answer()


@admin_router.callback_query(
    AdminAdStates.SELECT_STATUS, F.data.startswith("toggle_status:")
)
async def toggle_status(call: CallbackQuery, state: FSMContext):
    status = call.data.split(":")[1]
    data = await state.get_data()
    selected = data.get("selected_statuses", [])

    if status in selected:
        selected.remove(status)
    else:
        selected.append(status)

    await state.update_data(selected_statuses=selected, all_statuses=False)
    await call.message.edit_reply_markup(
        reply_markup=get_status_filter_keyboard(selected)
    )
    await call.answer()


@admin_router.callback_query(
    AdminAdStates.SELECT_STATUS, F.data == "all_statuses_selected"
)
async def all_statuses_selected(call: CallbackQuery, state: FSMContext):
    await state.update_data(all_statuses=True, selected_statuses=[])
    await call.message.answer("Tanlangan foydalanuvchilar holati: Barchasi")
    await call.message.answer(
        "Endi reklama matnini yuboring (matn, rasm, video, hujjat yoki media group):"
    )
    await state.set_state(AdminAdStates.WRITE_MESSAGE)
    await call.answer()


@admin_router.callback_query(AdminAdStates.SELECT_STATUS, F.data == "status_done")
async def status_done_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_statuses", [])
    if not selected:
        await call.answer("Iltimos, kamida bitta holat tanlang.", show_alert=True)
        return

    await call.message.answer(
        f"Tanlangan foydalanuvchilar holati: {', '.join(selected)}"
    )
    await call.message.answer(
        "Endi reklama matnini yuboring (matn, rasm, video, hujjat yoki media group):"
    )
    await state.set_state(AdminAdStates.WRITE_MESSAGE)
    await call.answer()


# Handle media group collection
@admin_router.message(AdminAdStates.WRITE_MESSAGE, F.media_group_id)
async def collect_media_group(message: Message, state: FSMContext):
    media_group_id = message.media_group_id
    user_id = message.from_user.id

    # Initialize media group storage for this user
    key = f"{user_id}_{media_group_id}"
    if key not in media_groups:
        media_groups[key] = []

    # Add message to media group
    media_groups[key].append(message)

    # Set a timer to process the media group (in case it's complete)
    async def process_media_group():
        await asyncio.sleep(1)  # Wait 1 second for more media
        if key in media_groups:
            messages = media_groups.pop(key)
            await state.update_data(
                media=messages, is_media_group=True, ad_text=messages[0].caption or ""
            )

            # Show advertisement preview and confirmation
            await send_advertisement_preview(
                message, messages, messages[0].caption or "", is_media_group=True
            )
            await state.set_state(AdminAdStates.CONFIRM_SEND)

    # Cancel previous timer if exists and start new one
    asyncio.create_task(process_media_group())


# Handle single media or text
@admin_router.message(
    AdminAdStates.WRITE_MESSAGE,
    F.content_type.in_(
        {
            "text",
            "photo",
            "video",
            "document",
            "audio",
            "voice",
            "video_note",
            "animation",
        }
    ),
)
async def receive_ad_content(message: Message, state: FSMContext):
    # Skip if this is part of a media group (handled separately)
    if message.media_group_id:
        return

    # Store the message
    ad_text = message.caption or message.text or ""
    await state.update_data(ad_text=ad_text, media=[message], is_media_group=False)

    # Show advertisement preview and confirmation
    await send_advertisement_preview(message, [message], ad_text, is_media_group=False)
    await state.set_state(AdminAdStates.CONFIRM_SEND)


# Handle confirmation callbacks
@admin_router.callback_query(AdminAdStates.CONFIRM_SEND, F.data == "confirm_send_yes")
async def confirm_send_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bot = call.bot  # Get bot instance from callback

    # Get filter information
    selected_regions = (
        data.get("selected_regions", []) if not data.get("all_regions") else []
    )
    selected_statuses = (
        data.get("selected_statuses", []) if not data.get("all_statuses") else []
    )

    # Get users based on filters
    users = await get_list_of_users(
        region_codes=selected_regions if not data.get("all_regions") else None,
        status=selected_statuses if not data.get("all_statuses") else None,
    )

    if not users:
        await call.message.answer(
            "Tanlangan shartlarga mos foydalanuvchilar topilmadi."
        )
        await call.answer()
        return

    # Start sending advertisements
    await call.message.answer(
        f"📤 Reklama {len(users)} ta foydalanuvchiga yuborilmoqda..."
    )

    success_count = 0
    failed_count = 0

    for user in users:
        try:
            # Extract user_id from user data structure
            # Adjust this based on your actual user data structure
            user_id = user.get("telegram_id")

            success = await send_ad_to_user(
                bot=bot,
                user_id=user_id,
                media=data.get("media", []),
                ad_text=data.get("ad_text", ""),
                is_media_group=data.get("is_media_group", False),
            )

            if success:
                success_count += 1
            else:
                failed_count += 1

            # Small delay to avoid rate limiting
            await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Error processing user {user}: {e}")
            failed_count += 1

    # Final report
    region_text = (
        "Barchasi"
        if data.get("all_regions")
        else ", ".join([name for code, name in REGIONS if code in selected_regions])
    )
    status_text = (
        "Barchasi" if data.get("all_statuses") else ", ".join(selected_statuses)
    )

    await call.message.answer(
        f"✅ Reklama yuborish yakunlandi!\n"
        f"📍 Regions: {region_text}\n"
        f"📌 Status: {status_text}\n"
        f"📊 Muvaffaqiyatli: {success_count}\n"
        f"❌ Muvaffaqiyatsiz: {failed_count}\n"
        f"👥 Jami: {len(users)}"
    )
    await call.answer("Reklama muvaffaqiyatli yuborildi!")
    await state.clear()


@admin_router.callback_query(AdminAdStates.CONFIRM_SEND, F.data == "confirm_send_no")
async def confirm_send_no(call: CallbackQuery, state: FSMContext):
    await call.message.answer("❌ Reklama yuborish bekor qilindi.")
    await call.answer()
    await state.clear()


@admin_router.callback_query(
    AdminAdStates.CONFIRM_SEND, F.data == "confirm_send_rewrite"
)
async def confirm_send_rewrite(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "🔄 Reklama matnini qayta yozing (matn, rasm, video, hujjat yoki media group):"
    )
    await call.answer()
    await state.set_state(AdminAdStates.WRITE_MESSAGE)


@admin_router.callback_query(AdminAdStates.CONFIRM_SEND, F.data == "confirm_send_back")
async def confirm_send_back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_statuses", [])

    await call.message.answer(
        "⬅️ Status tanloviga qaytdingiz. Foydalanuvchilar holatini tanlang:",
        reply_markup=get_status_filter_keyboard(selected),
    )
    await call.answer()
    await state.set_state(AdminAdStates.SELECT_STATUS)


@admin_router.message(
    AdminAdStates.CONFIRM_SEND, F.text.lower().in_(["✅ ha", "❌ yo'q", "ha", "yo'q"])
)
async def confirm_send_text_fallback(message: Message, state: FSMContext):
    """Fallback for users who type instead of using buttons"""
    if message.text.lower() in ["❌ yo'q", "yo'q"]:
        await message.answer("❌ Reklama yuborish bekor qilindi.")
        await state.clear()
    else:
        # Redirect to the main confirmation handler
        await confirm_send_yes_text(message, state)


async def confirm_send_yes_text(message: Message, state: FSMContext):
    """Handle text confirmation"""
    data = await state.get_data()
    bot = message.bot

    # Get filter information
    selected_regions = (
        data.get("selected_regions", []) if not data.get("all_regions") else []
    )
    selected_statuses = (
        data.get("selected_statuses", []) if not data.get("all_statuses") else []
    )

    users = await get_list_of_users(
        region_codes=selected_regions if not data.get("all_regions") else None,
        status=selected_statuses if not data.get("all_statuses") else None,
    )

    if not users:
        await message.answer("Tanlangan shartlarga mos foydalanuvchilar topilmadi.")
        return

    await message.answer(f"📤 Reklama {len(users)} ta foydalanuvchiga yuborilmoqda...")
    print(users)
    print(type(users))
    success_count = 0
    failed_count = 0

    for user in users:
        try:
            print(f"Processing user: {user}")
            user_id = user.get("telegram_id")
            print(f"Sending ad to user: {user_id}")

            success = await send_ad_to_user(
                bot=bot,
                user_id=int(user_id),
                media=data.get("media", []),
                ad_text=data.get("ad_text", ""),
                is_media_group=data.get("is_media_group", False),
            )

            if success:
                success_count += 1
            else:
                failed_count += 1

            await asyncio.sleep(0.5)

        except Exception as e:
            logger.error(f"Error processing user {user}: {e}")
            failed_count += 1

    region_text = (
        "Barchasi"
        if data.get("all_regions")
        else ", ".join([name for code, name in REGIONS if code in selected_regions])
    )
    status_text = (
        "Barchasi" if data.get("all_statuses") else ", ".join(selected_statuses)
    )

    await message.answer(
        f"✅ Reklama yuborish yakunlandi!\n"
        f"📍 Regions: {region_text}\n"
        f"📌 Status: {status_text}\n"
        f"📊 Muvaffaqiyatli: {success_count}\n"
        f"❌ Muvaffaqiyatsiz: {failed_count}\n"
        f"👥 Jami: {len(users)}"
    )
    await state.clear()


# Handle any other message types in WRITE_MESSAGE state
@admin_router.message(AdminAdStates.WRITE_MESSAGE)
async def handle_unsupported_content(message: Message, state: FSMContext):
    await message.answer(
        "Ushbu kontent turi qo'llab-quvvatlanmaydi. "
        "Iltimos, matn, rasm, video yoki hujjat yuboring."
    )
