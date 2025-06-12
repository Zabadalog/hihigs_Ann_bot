# handlers/callbacks.py
from aiogram import types, Dispatcher

from .bot_commands import status_command, register_command

async def confirm_tracking_callback(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Отслеживание подтверждено.")


async def status_callback(call: types.CallbackQuery):
    await call.answer()
    await status_command(call.message)


async def register_callback(call: types.CallbackQuery):
    await call.answer()
    await register_command(call.message)

def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_tracking_callback, text="confirm_tracking")
    dp.register_callback_query_handler(status_callback, text="status")
    dp.register_callback_query_handler(register_callback, text="register")
