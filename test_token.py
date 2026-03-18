import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
from config import BOT_TOKEN, validate_config


async def main():
    validate_config()
    bot = Bot(BOT_TOKEN)
    try:
        me = await bot.get_me()
        print("ISHLADI")
        print("Bot username:", me.username)
        print("Bot id:", me.id)
    except TelegramUnauthorizedError:
        print("TOKEN XATO yoki ESKI")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
