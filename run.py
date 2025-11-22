import asyncio
from aiogram import Bot, Dispatcher

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv
import os

from app.handlers import router

async def main():
    load_dotenv()
    bot = Bot(os.getenv('TG_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())