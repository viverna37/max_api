# Определяем группу состояний FSM для процесса рассылки
from maxapi.context import State, StatesGroup


class BroadcastStates(StatesGroup):
    WAIT_TEXT = State()  # Ожидание ввода текста для текстовой рассылки
    WAIT_PHOTO = State()  # Ожидание фото для рассылки с фото
    WAIT_PHOTO_TEXT = State()  # Ожидание текста (подписи) после получения фото
    WAIT_VIDEO = State()  # Ожидание видео для рассылки с видео
    WAIT_VIDEO_TEXT = State()  # Ожидание текста (описания) после получения видео
