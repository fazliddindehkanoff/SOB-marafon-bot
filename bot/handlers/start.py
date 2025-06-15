from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.constants import Messages
from bot.buttons import get_language_options, get_main_menu_keyboards
from bot.selectors import get_user
from bot.states import UserStates

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.from_user.id)

    if user:
        lang_code = user.language
        await message.answer(
            Messages.main_menu.value.get(lang_code),
            reply_markup=get_main_menu_keyboards(language_code=lang_code),
        )
        await state.clear()
    else:
        await message.answer(
            Messages.greeting_uz.value + "\n\n" + Messages.greeting_ru.value,
            reply_markup=get_language_options(),
        )
        await state.set_state(UserStates.GET_LANGUAGE)
