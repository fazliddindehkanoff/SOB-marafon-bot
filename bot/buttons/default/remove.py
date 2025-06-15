from aiogram.types import ReplyKeyboardRemove


async def remove_keyboard():
    """
    Function to remove the keyboard from the chat.
    Returns a ReplyKeyboardRemove object to remove the keyboard.
    """
    return ReplyKeyboardRemove()
