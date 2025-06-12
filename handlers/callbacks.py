# handlers/callbacks.py
from aiogram import types, Dispatcher

async def confirm_tracking_callback(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Отслеживание подтверждено.")

def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_tracking_callback, text="confirm_tracking")
