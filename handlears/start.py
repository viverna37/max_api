from maxapi import F
from maxapi.types import BotStarted, LinkButton, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from database.db import db
from database.repository.main_repository import Repository
from config import dp


@dp.bot_started()
async def on_bot_started(event: BotStarted):
    campaign_id = event.payload.split("_")[1] if event.payload else None

    async with db.session() as session:
        repo = Repository(session)

        status = await repo.user_repository.create(
            max_id=event.user.user_id,
            full_name=event.user.full_name,
            username=str(event.chat_id),
            campaign_id=campaign_id
        )

    if status == "ok":
        async with db.session() as session:
            repo = Repository(session)
            text = await repo.default_repository.get_value("message")
            link = await repo.default_repository.get_value("link")

        builder = InlineKeyboardBuilder()
        builder.row(
            LinkButton(text="Перейти", url=link)
        )
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=text,
            attachments=[builder.as_markup()]
        )
    else:
        async with db.session() as session:
            repo = Repository(session)

            links = await repo.campaign_repository.get_campaign(campaign_id)
            text = await repo.campaign_repository.get_campaign(campaign_id=campaign_id)

        builder = InlineKeyboardBuilder()
        if len(links.links) == 1:
            for i in links.links:
                builder.row(LinkButton(text=f"Канал", url=i))
        else:
            for i in enumerate(links.links):
                builder.row(LinkButton(text=f"{i[0]+1}. Канал", url=i[1]))


        await repo.campaign_repository.increment(campaign_id=campaign_id)
        await event.bot.send_message(
                chat_id=event.chat_id,
                text=text.message,
                attachments=[builder.as_markup()]
            )






