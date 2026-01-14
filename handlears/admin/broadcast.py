from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated, MessageCallback, PhotoAttachmentPayload, CallbackButton
from maxapi.types.attachments import Image
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from bot import bot
from database.db import db
from database.repository.main_repository import Repository
from config import dp
from keyboards.ikb import IKB
from states.admin_broadcast import BroadcastStates


@dp.message_callback(F.callback.payload == "broadcast")
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    await event.message.answer(text="📢 Выберите схему рассылки:", attachments=[IKB.Admin.broadcast_type_keyboard()])


@dp.message_callback(F.callback.payload == "broadcast_target")
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    async with db.session() as session:
        repo = Repository(session)
        all_campaign = await repo.campaign_repository.get_all_campaigns()
    builder = InlineKeyboardBuilder()
    for i in all_campaign:
        builder.row(CallbackButton(text=i.name, payload=f"target_{i.id}"))
    await event.message.answer(text="📢 Выберите кампанию для рассылки:", attachments=[builder.as_markup()])


@dp.message_callback(F.callback.payload.startswith("target"))
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    campaign_id = event.callback.payload.split("_")[-1]
    await event.message.answer(text="📢 Выберите тип рассылки:", attachments=[IKB.Admin.broadcast_keyboard(campaign_id)])


@dp.message_callback(F.callback.payload == "broadcast_all")
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    await event.message.answer(text="📢 Выберите тип рассылки:", attachments=[IKB.Admin.broadcast_keyboard("all")])


# Обработчик нажатия кнопки "Рассылка" – запрашиваем текст для рассылки
@dp.message_callback(F.callback.payload.startswith("broadcast_text_"))
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    param = event.callback.payload.split("_")[-1]
    await context.set_state(BroadcastStates.WAIT_TEXT)
    await event.message.answer(text="📢 Введите текст сообщения для рассылки:")
    await context.update_data(param=param)


# Обработчик нажатия кнопки "Рассылка с фото" – запрашиваем фото
@dp.message_callback(F.callback.payload.startswith('broadcast_photo_'))
async def on_broadcast_photo_button(event: MessageCallback, context: MemoryContext):
    param = event.callback.payload.split("_")[-1]
    await context.set_state(BroadcastStates.WAIT_PHOTO)
    await event.message.answer(
        text="🖼️ Пришлите фотографию, которую нужно разослать всем пользователям.")
    await context.update_data(param=param)

# Обработчик получения **текста** для текстовой рассылки (состояние WAIT_TEXT)
@dp.message_created(BroadcastStates.WAIT_TEXT)
async def handle_broadcast_text(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    if data.get("param") == "all":
        async with db.session() as session:
            repo = Repository(session)
            user_ids = await repo.user_repository.get_users()
    else:
        async with db.session() as session:
            repo = Repository(session)
            user_ids = await repo.user_repository.get_users_by_campaign_id(data.get("param"))
    # Получаем введённый текст от администратора
    broadcast_text = event.message.body.text
    # Инициализируем счётчики результатов
    delivered = 0
    failed = 0

    # Рассылаем текст всем пользователям из списка
    for uid in user_ids:
        try:
            await bot.send_message(chat_id=uid, text=broadcast_text)
            delivered += 1
        except Exception as e:
            failed += 1
    # Выходим из состояния и отправляем администратору отчёт
    await context.clear()  # Сброс контекста FSM (очистка состояния и данных):contentReference[oaicite:2]{index=2}
    await event.message.answer(
        text=f"✅ Рассылка текста завершена.\nУспешно отправлено: {delivered}\nНе доставлено: {failed}"
    )


# Обработчик получения **фото** для рассылки (состояние WAIT_PHOTO)
@dp.message_created(BroadcastStates.WAIT_PHOTO)
async def handle_broadcast_photo(event: MessageCreated, context: MemoryContext):
    if event.message.body.attachments:
        photo_attachment = event.message.body.attachments[0]
        photo_id = photo_attachment.payload.photo_id
        photo_url = photo_attachment.payload.url
        photo_token = photo_attachment.payload.token
        await context.update_data(photo_id=photo_id, photo_token=photo_token, photo_url=photo_url)
        await context.set_state(BroadcastStates.WAIT_PHOTO_TEXT)
        await event.message.answer(
            text="📷 Фото получено. Теперь отправьте текст, который будет добавлен к фото при рассылке:"
        )
    else:
        await event.message.answer(
            text="❗ Пожалуйста, отправьте фотографию для рассылки."
        )


# Обработчик получения **текста** после фото (состояние WAIT_PHOTO_TEXT)
@dp.message_created(BroadcastStates.WAIT_PHOTO_TEXT)
async def handle_broadcast_photo_text(event: MessageCreated, context: MemoryContext):
    caption_text = event.message.body.text
    data = await context.get_data()
    if data.get("param") == "all":
        async with db.session() as session:
            repo = Repository(session)
            user_ids = await repo.user_repository.get_users()
    else:
        async with db.session() as session:
            repo = Repository(session)
            user_ids = await repo.user_repository.get_users_by_campaign_id(data.get("param"))

    photo_id = data.get('photo_id')
    photo_url = data.get('photo_url')
    photo_token = data.get('photo_token')
    delivered = 0
    failed = 0
    for uid in user_ids:
        try:

            image = Image(
                type="image",
                payload=PhotoAttachmentPayload(
                    photo_id=photo_id,
                    url=photo_url,
                    token=photo_token
                )
            )

            await bot.send_message(
                chat_id=uid,
                text=caption_text,
                attachments=[image]
            )

            delivered += 1
        except Exception as e:
            failed += 1

    await context.clear()
    await event.message.answer(
        text=f"✅ Рассылка фото завершена.\nУспешно: {delivered}\nНе доставлено: {failed}"
    )

