from maxapi import F
from maxapi.types import BotStarted, CallbackButton, LinkButton, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from database.db import db
from database.models import Campaign
from database.repository.main_repository import Repository
from config import dp
from keyboards.ikb import IKB


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
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=text,
            attachments=[IKB.User.get_verification_keyboard()]
        )
    else:
        async with db.session() as session:
            repo = Repository(session)
            text = await repo.campaign_repository.get_campaign(campaign_id=campaign_id)
            await repo.campaign_repository.increment(campaign_id=campaign_id)
            await event.bot.send_message(
                chat_id=event.chat_id,
                text=text.message,
                attachments=[IKB.User.get_verification_keyboard()]
            )


@dp.message_callback(F.callback.payload == "im_human")
async def handle_button(event: MessageCallback):
    async with db.session() as session:
        repo = Repository(session)
        user_data = await repo.user_repository.get_user_by_telegram_id(event.callback.user.user_id)

    if user_data.campaign_id == 0:
        async with db.session() as session:
            repo = Repository(session)
            link = await repo.default_repository.get_value("link")

        builder = InlineKeyboardBuilder()
        builder.row(
            LinkButton(text="Перейти", url=link)
        )
        await event.message.answer(text=f"Супер! Теперь верю. Ссылка по кнопке ниже",
                                   attachments=[builder.as_markup()])
    else:
        async with db.session() as session:
            repo = Repository(session)
            links = await repo.campaign_repository.get_campaign(user_data.campaign_id)
            builder = InlineKeyboardBuilder()
            for i in links.links:
                builder.row(LinkButton(text="Перейти", url=i))

            await event.message.answer(text=f"Супер! Теперь верю. Ссылка по кнопке ниже",
                                       attachments=[builder.as_markup()])



