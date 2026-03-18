import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError

from config import BOT_TOKEN, validate_config
from app.handlers.admin import router as admin_router
from app.handlers.user import router as user_router
from app.services.database import init_db


async def main():
    validate_config()
    logging.basicConfig(level=logging.INFO)
    init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(user_router)

    try:
        me = await bot.get_me()
        print(f"Bot ishga tushdi: @{me.username}")
        await dp.start_polling(bot)
    except TelegramUnauthorizedError:
        print(
            "XATO: Telegram token noto'g'ri yoki bekor qilingan. "
            "@BotFather dan yangi token olib, .env ichidagi BOT_TOKEN ni almashtiring."
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
