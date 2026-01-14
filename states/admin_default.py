from maxapi.context import StatesGroup, State


class DefaultStates(StatesGroup):
    WAIT_LINK = State()
    WAIT_MESSAGE = State()