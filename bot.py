from config import load_config, dp
import asyncio
import logging
from maxapi import Bot, Dispatcher
from database.db import db
from handlears import auto_import_handlers

logging.basicConfig(level=logging.INFO)

config = load_config()
bot = Bot(config.max_bot.token)


async def main():
    await db.init(config.db.url)
    await db.create_tables()
    auto_import_handlers()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
