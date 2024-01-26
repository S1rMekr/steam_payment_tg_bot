import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, shipping_query, successful_payment
from aiogram.enums.content_type import ContentType
from app import handlers
from config import Config, load_config

logger = logging.getLogger(__name__)

async def main():

    config: Config = load_config()

    logging.basicConfig(level=logging.INFO)

    logger.info("Starting bot")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

    dp= Dispatcher()

    dp.include_routers(
        handlers.router,
        )

    

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())