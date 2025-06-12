import logging
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import register_all_handlers
from handlers.logging_config import logger


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_all_handlers(dp)

if __name__ == '__main__':
    logger.info("Бот запущен")
    executor.start_polling(dp, skip_updates=True)