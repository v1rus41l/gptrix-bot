import asyncio
from aiogram import Dispatcher

from bot_create import bot

from app.handlers import router


async def main():   
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())