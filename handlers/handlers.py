from aiogram import Dispatcher
from .bot_commands import register_handlers
from .callbacks import register_callbacks

def register_all_handlers(dp: Dispatcher):
    register_handlers(dp)
    register_callbacks(dp)

