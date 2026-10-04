import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, farmer, driver, prices

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(farmer.router)
    dp.include_router(driver.router)
    dp.include_router(prices.router)
    return dp


async def main():
    logging.basicConfig(level=logging.INFO)
    token = os.getenv("TELEGRAM_BOT_TOKEN", "mock_bot_token_for_development")
    bot = Bot(token=token)
    dp = create_dispatcher()
    logger.info("Starting HosilBozor aiogram 3 bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
