import os
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

from bot.constants import Buttons, Messages
from bot.buttons import (
    get_contact,
    get_main_menu_keyboards,
    get_region_buttons,
    get_payment_keyboard,
    get_terms_keyboard,
    get_change_buttons,
    get_language_options,
    remove_keyboard,
    get_link_button,
    get_tarif_buttons,
)
from bot.states import UserStates
from bot.services import create_user, update_user
from bot.selectors import (
    get_admin_username,
    get_all_faq,
    get_user_language,
    get_tarif,
    get_last_marathon,
    get_chosen_tarif_private_link,
)

load_dotenv()
user_router = Router()


@user_router.message(UserStates.GET_LANGUAGE)
async def set_language(message: types.Message, state: FSMContext):
    language_code = "uz" if message.text == Buttons.uzbek_lang.value else "ru"
    await state.update_data(language_code=language_code)
    remove_btn = await remove_keyboard()

    await message.answer(
        Messages.send_name.value.get(language_code),
        reply_markup=remove_btn,
    )
    await state.set_state(UserStates.GET_NAME)


@user_router.message(UserStates.GET_NAME)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    language_code = data.get("language_code", "uz")
    await message.answer(
        Messages.choose_region.value.get(language_code),
        reply_markup=get_region_buttons(),
    )
    await state.set_state(UserStates.GET_REGION)


@user_router.callback_query(UserStates.GET_REGION)
async def get_region_callback(call: CallbackQuery, state: FSMContext):
    region = call.data.split("_")[1]
    await call.message.delete()
    data = await state.get_data()
    language_code = data.get("language_code", "uz")

    if call.data == "other_region":
        await call.message.answer(
            Messages.region_title.value.get(language_code),
        )
        return

    await state.update_data(region=region)
    await call.message.answer(
        Messages.send_phone_number.value.get(language_code),
        reply_markup=get_contact(
            Buttons.send_phone_number.value.get(language_code),
        ),
    )
    await state.set_state(UserStates.GET_PHONE)


@user_router.message(UserStates.GET_REGION)
async def get_region_message(message: types.Message, state: FSMContext):
    region = message.text
    await state.update_data(region=region)
    data = await state.get_data()
    language_code = data.get("language_code", "uz")

    await message.answer(
        Messages.send_phone_number.value.get(language_code),
        reply_markup=get_contact(
            Buttons.send_phone_number.value.get(language_code),
        ),
    )
    await state.set_state(UserStates.GET_PHONE)


@user_router.message(UserStates.GET_PHONE, F.text.regexp(r"^\+998\d{9}$"))
@user_router.message(UserStates.GET_PHONE, F.contact)
async def handle_phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language_code = data.get("language_code", "uz")

    phone_number = (
        message.contact.phone_number if message.contact else message.text
    )  # noqa
    await state.update_data(phone_number=phone_number)

    user_data = await state.get_data()
    chat_id = message.from_user.id

    await create_user(
        chat_id=chat_id,
        name=user_data["full_name"],
        region=user_data["region"],
        phone_number=user_data["phone_number"],
        language_code=user_data["language_code"],
    )
    marafon = await get_last_marathon()
    public_offer_link = ""
    if language_code == "uz":
        public_offer_link = marafon.public_offer_link_uz
    else:
        public_offer_link = marafon.public_offer_link_ru

    await message.answer(
        Messages.terms.value.get(language_code).format(public_offer_link),
        reply_markup=get_terms_keyboard(language_code),
    )


@user_router.callback_query(F.data == "accept_terms")
@user_router.callback_query(F.data == "back_to_payment")
async def handle_accept_terms(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    language_code = await get_user_language(call.from_user.id)
    last_marathon = await get_last_marathon()
    text = ""
    if language_code == "uz":
        text += f"Marafon haqida ma'lumot:\n\n{last_marathon.description_uz}"
    else:
        text += f"Информация о марафоне:\n\n{last_marathon.description_ru}"
    await call.message.answer(
        text,
        reply_markup=await get_tarif_buttons(
            language_code=language_code, marathon_id=last_marathon.id
        ),
    )


@user_router.callback_query(F.data.startswith("tarif_"))
async def handle_tarif_selection(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    tarif_id = call.data.split("_")[1]
    language_code = await get_user_language(call.from_user.id)
    tarif = await get_tarif(tarif_id)
    await update_user(
        chat_id=call.from_user.id,
        chosen_tarif=tarif,
    )

    await call.message.answer_invoice(
        title=tarif["name_uz"] if language_code == "uz" else tarif["name_ru"],
        description=(
            tarif["description_uz"]
            if language_code == "uz"
            else tarif["description_ru"]  # noqa
        ),
        payload="course-access",
        provider_token=os.getenv("PROVIDER_TOKEN"),
        currency="UZS",
        prices=[
            types.LabeledPrice(
                label=tarif["name_uz"],
                amount=tarif["price"] * 100,
            )
        ],
        start_parameter="course-payment",
        reply_markup=get_payment_keyboard(language_code=language_code),
    )


@user_router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@user_router.message(F.successful_payment)
async def successful_payment(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)
    private_link = await get_chosen_tarif_private_link(message.from_user.id)
    await message.answer(
        Messages.payment_successful.value.get(language_code),
        reply_markup=get_link_button(
            private_link,
            Buttons.join_group.value.get(language_code),
        ),
    )
    update_user(
        chat_id=message.from_user.id,
        is_subscribed=True,
    )
    await message.answer(
        Messages.main_menu.value.get(language_code),
        reply_markup=get_main_menu_keyboards(language_code=language_code),
    )


@user_router.message(
    F.text.in_([Buttons.faq.value["uz"], Buttons.faq.value["ru"]]),
)
async def faq_handler(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)
    msg = await get_all_faq(language=language_code)
    await message.answer(msg)


@user_router.message(
    F.text.in_([Buttons.contact.value["uz"], Buttons.contact.value["ru"]])
)
async def contact_admin_handler(message: types.Message, state: FSMContext):
    admin_username = await get_admin_username()
    await message.answer(f"Admin: @{admin_username}")


@user_router.message(
    F.text.in_([Buttons.settings.value["uz"], Buttons.settings.value["ru"]])
)
async def settings_handler(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)
    await message.answer(
        Messages.settings.value.get(language_code),
        reply_markup=get_change_buttons(language_code),
    )


@user_router.message(
    F.text.in_(
        [
            Buttons.change_language.value["uz"],
            Buttons.change_language.value["ru"],
        ]
    )
)
async def change_language(message: types.Message, state: FSMContext):
    await message.answer(
        "🇺🇿 O'zbekcha yoki 🇷🇺 Русский tilini tanlang:",
        reply_markup=get_language_options(),
    )
    await state.set_state(UserStates.CHANGE_LANGUAGE)


@user_router.message(UserStates.CHANGE_LANGUAGE)
async def change_language_handler(message: types.Message, state: FSMContext):
    if message.text == Buttons.uzbek_lang.value:
        language_code = "uz"
    elif message.text == Buttons.russian_lang.value:
        language_code = "ru"
    else:
        await message.answer("Iltimos, tilni to'g'ri tanlang.")
        return

    await update_user(
        chat_id=message.from_user.id,
        language=language_code,
    )
    await state.update_data(language_code=language_code)
    await message.answer(
        Messages.language_changed.value.get(language_code),
        reply_markup=get_main_menu_keyboards(language_code=language_code),
    )
    await state.clear()


@user_router.message(
    F.text.in_(
        [
            Buttons.change_phone.value["uz"],
            Buttons.change_phone.value["ru"],
        ]
    )
)
async def change_phone(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)
    await message.answer(
        Messages.send_phone_number.value.get(language_code),
        reply_markup=get_contact(
            Buttons.send_phone_number.value.get(language_code),
        ),
    )
    await state.set_state(UserStates.CHANGE_PHONE)


@user_router.message(UserStates.CHANGE_PHONE, F.text.regexp(r"^\+998\d{9}$"))
@user_router.message(UserStates.CHANGE_PHONE, F.contact)
async def handle_change_phone(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)

    phone_number = (
        message.contact.phone_number if message.contact else message.text
    )  # noqa
    await update_user(
        chat_id=message.from_user.id,
        phone_number=phone_number,
    )

    await message.answer(
        Messages.phone_changed.value.get(language_code),
        reply_markup=get_main_menu_keyboards(language_code=language_code),
    )
    await state.clear()


@user_router.message(
    F.text.in_(
        [
            Buttons.change_region.value["uz"],
            Buttons.change_region.value["ru"],
        ]
    )
)
async def change_region(message: types.Message, state: FSMContext):
    await message.answer(
        Messages.choose_region.value.get("uz"),
        reply_markup=get_region_buttons(),
    )
    await state.set_state(UserStates.CHANGE_REGION)


@user_router.callback_query(UserStates.CHANGE_REGION)
async def change_region_callback(call: CallbackQuery, state: FSMContext):
    region = call.data.split("_")[1]
    await call.message.delete()
    await state.update_data(region=region)

    language_code = await get_user_language(call.from_user.id)
    await update_user(
        chat_id=call.from_user.id,
        region=region,
    )

    await call.message.answer(
        Messages.region_changed.value.get(language_code),
        reply_markup=get_main_menu_keyboards(language_code=language_code),
    )
    await state.clear()


@user_router.message(F.text == Buttons.back.value["uz"])
@user_router.message(F.text == Buttons.back.value["ru"])
async def back_to_main_menu(message: types.Message, state: FSMContext):
    language_code = await get_user_language(message.from_user.id)
    await message.answer(
        Messages.main_menu.value.get(language_code),
        reply_markup=get_main_menu_keyboards(language_code=language_code),
    )
    await state.clear()
