from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_tracking_confirmation_keyboard():
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Подтвердить отслеживание", callback_data="confirm_tracking")
    )
    return keyboard

def get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Статус", callback_data="status"),
        InlineKeyboardButton("Регистрация", callback_data="register"),
    )
    return keyboard
