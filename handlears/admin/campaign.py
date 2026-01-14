from marshmallow.fields import List
from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCallback, MessageCreated
from sqlalchemy import Sequence

from database.db import db
from database.models import Campaign
from database.repository.main_repository import Repository
from config import dp
from states.admin_campaign import CreateCampaignStates



@dp.message_callback(F.callback.payload == "create_campaign")
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    await event.message.answer(text="📢 Введите имя для новой кампании. Это условное название только для аминистрации")
    await context.set_state(CreateCampaignStates.WAIT_NAME)


@dp.message_created(CreateCampaignStates.WAIT_NAME)
async def handle_broadcast_video_text(event: MessageCreated, context: MemoryContext):
    await event.message.answer(text="📢 Введите ссылки для новой кампании. Эти ссылки будут высылаться пользователю после подтверждения его человечности"
                                    "\n\nОбязательно https://\nВводи через ентер")
    caption_text = event.message.body.text

    await context.update_data(name=caption_text)
    await context.set_state(CreateCampaignStates.WAIT_LINKS)

@dp.message_created(CreateCampaignStates.WAIT_LINKS)
async def handle_broadcast_video_text(event: MessageCreated, context: MemoryContext):
    await event.message.answer(text="📢 Стартовое сообщение, оно будет приходить пользователю при запуске бота")
    caption_text = event.message.body.text.split("\n")

    await context.update_data(links=caption_text)
    await context.set_state(CreateCampaignStates.WAIT_START_MESSAGE)

@dp.message_created(CreateCampaignStates.WAIT_START_MESSAGE)
async def handle_broadcast_video_text(event: MessageCreated, context: MemoryContext):
    start_msg = event.message.body.text
    data = await context.get_data()
    async with db.session() as session:
        repo = Repository(session)
        id = await repo.campaign_repository.create(name=data.get("name"), links=data.get("links"), start_msg=start_msg)

    await event.message.answer(text=f"Усешно создана новая кампания {data.get("name")}\n\n"
                                    f""
                                    f"Уникальная ссылка для кампании ниже\n"
                                    f"https://max.ru/id631109970212_bot?start=campaign_{id.id}")
    await context.clear()

@dp.message_callback(F.callback.payload == "my_campaign")
async def on_broadcast_text_button(event: MessageCallback, context: MemoryContext):
    async with db.session() as session:
        repo = Repository(session)
        campaigns = await repo.campaign_repository.get_all_campaigns()

    msg = "Статистика по кампаниям\n\n"

    for i in campaigns:
        msg += f"Кампания: {i.name}\nПереходов: {i.count_transitions}\nСсылка: https://max.ru/id631109970212_bot?start=campaign_{i.id}\n\n"

    await event.message.answer(text=msg)