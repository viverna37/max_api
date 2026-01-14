from maxapi import F
from maxapi.types import MessageCreated

from config import dp
from keyboards.ikb import IKB

@dp.message_created(F.message.body.text == "/admin")
async def on_message(event: MessageCreated):
    await event.message.answer(text="Админ панель", attachments=[IKB.Admin.get_admin_keyboard()])