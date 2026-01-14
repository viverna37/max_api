# Определяем группу состояний FSM для процесса создания кампании
from maxapi.context import State, StatesGroup


class CreateCampaignStates(StatesGroup):
    WAIT_NAME = State()  # Ожидание ввода названия кампании
    WAIT_LINKS = State()  # Ожидание ссылок для выдачи
    WAIT_START_MESSAGE = State()  # Ожидание стартового сообщения
