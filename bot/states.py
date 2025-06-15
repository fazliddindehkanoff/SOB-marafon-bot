from aiogram.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    GET_LANGUAGE = State()
    GET_NAME = State()
    GET_REGION = State()
    GET_PHONE = State()
    CHANGE_PHONE = State()
    CHANGE_LANGUAGE = State()
    CHANGE_REGION = State()


class AdminAdStates(StatesGroup):
    SELECT_STATUS = State()
    SELECT_REGIONS = State()
    WRITE_MESSAGE = State()
    CONFIRM_SEND = State()
