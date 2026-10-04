import asyncio
import logging
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, farmer, driver, prices

logger = logging.getLogger("hosilbozor_bot")


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(farmer.router)
    dp.include_router(driver.router)
    dp.include_router(prices.router)
    return dp


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish va asosiy menyu"),
        BotCommand(command="prices", description="Bozorlardagi kunlik narxlar"),
        BotCommand(command="harvest", description="Yangi hosil e'lon qilish (60 soniya)"),
        BotCommand(command="cargo", description="Yuk tashish topshiriqlari"),
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logger.warning(f"Failed to set bot commands: {e}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    token = os.getenv("TELEGRAM_BOT_TOKEN", "8832587255:AAG_FNR3jpgPKWNPoxuGmgg3cmkzqmN4Lvs")
    bot = Bot(token=token)
    dp = create_dispatcher()

    # Drop any pending updates and ensure clean polling
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)

    bot_info = await bot.get_me()
    logger.info(f"✅ HosilBozor Bot muvaffaqiyatli ishga tushdi: @{bot_info.username} ({bot_info.first_name})")
    print(f"\n🌾 HosilBozor Telegram Boti ishga tushdi: @{bot_info.username}\n")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
