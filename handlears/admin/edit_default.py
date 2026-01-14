from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCallback, MessageCreated

from database.db import db
from database.repository.main_repository import Repository
from config import dp
from states.admin_default import DefaultStates



@dp.message_callback(F.callback.payload == "edit_link")  

async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    # Установить состояние ожидания текста и запросить у пользователя ввод
    await event.message.answer(text="📢 Введите новую ссылку\nОбязательно https://")
    await context.set_state(DefaultStates.WAIT_LINK)


@dp.message_created(DefaultStates.WAIT_LINK)
async def handle_broadcast_video_text(event: MessageCreated, context: MemoryContext):
    caption_text = event.message.body.text
    async with db.session() as session:
        repo = Repository(session)
        await repo.default_repository.update_default_value(name="link", value=caption_text)

    await event.message.answer(text="Ссылка изменена!")
    await context.clear()


@dp.message_callback(F.callback.payload == "edit_message")  

async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    # Установить состояние ожидания текста и запросить у пользователя ввод
    await event.message.answer(text="📢 Введите новое стартовое сообщение")
    await context.set_state(DefaultStates.WAIT_MESSAGE)


@dp.message_created(DefaultStates.WAIT_MESSAGE)
async def handle_broadcast_video_text(event: MessageCreated, context: MemoryContext):
    caption_text = event.message.body.text

    async with db.session() as session:
        repo = Repository(session)
        await repo.default_repository.update_default_value(name="link", value=caption_text)

    await event.message.answer(text="Стартовое сообщение успешно изменено")
    await context.clear()