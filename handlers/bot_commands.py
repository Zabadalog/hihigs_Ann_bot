from aiogram import types
from aiogram.dispatcher import Dispatcher
import yadisk

from db.engine import SessionLocal
from db.models import User

# — /start
async def start_command(message: types.Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id)
            db.add(user)
            db.commit()
            await message.answer("Вы успешно зарегистрированы!")
        else:
            await message.answer("Вы уже зарегистрированы.")
    finally:
        db.close()

# — /status
async def status_command(message: types.Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            return await message.answer("Вы не зарегистрированы. Используйте /register.")
        if user.yadisk_token:
            await message.answer(f"Вы зарегистрированы. Ваш токен Яндекс Диска: {user.yadisk_token}")
        else:
            await message.answer("Вы зарегистрированы, но токен Яндекс Диска отсутствует. Используйте /register и /token.")
    finally:
        db.close()

# — /register
async def register_command(message: types.Message):
    text = (
        "Процесс получения токена Яндекс.Диска:\n\n"
        "1. Перейдите на https://oauth.yandex.ru/client/new\n"
        "2. Название — любое, платформа — Веб-сервисы\n"
        "3. Redirect URI — https://oauth.yandex.ru/verification_code\n"
        "4. Права: чтение/запись всего Диска, доступ к папке приложения и др.\n"
        "5. Получите client_id и перейдите по ссылке:\n"
        "   https://oauth.yandex.ru/authorize?response_type=token&client_id=<ВАШ client_id>\n\n"
        "После получения токена введите:\n"
        "/token <ВАШ_ТОКЕН>"
    )
    await message.answer(text)

# — /token
async def token_command(message: types.Message):
    # извлекаем аргумент (fallback для FakeMessage)
    try:
        raw = message.get_args().strip()
    except AttributeError:
        parts = message.text.split(maxsplit=1)
        raw = parts[1].strip() if len(parts) > 1 else ""

    if not raw:
        return await message.answer("Пожалуйста, укажите токен: /token <ТОКЕН>")

    # проверяем токен, при любой ошибке считаем его неверным
    valid = False
    try:
        y = yadisk.YaDisk(token=raw)
        valid = y.check_token()
    except Exception:
        valid = False

    if not valid:
        return await message.answer("Недействительный токен. Попробуйте снова.")

    # если дошли сюда — токен валидный, сохраняем
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            return await message.answer("Вы не зарегистрированы. Сначала используйте /start.")
        user.yadisk_token = raw
        db.commit()
        await message.answer("Токен успешно сохранён!")
    finally:
        db.close()

        # /help
async def help_command(message: types.Message):
    help_text = (
        "Доступные команды:\n\n"
        "/start — зарегистрироваться в боте\n"
        "/status — узнать свой статус и токен Яндекс.Диска\n"
        "/register — инструкция по получению токена Яндекс.Диска\n"
        "/token <ТОКЕН> — сохранить полученный токен\n"
        "/add <ПУТЬ> — добавить папку для отслеживания\n"
        "/help — показать это сообщение"
    )
    await message.answer(help_text)

# — /add
async def add_command(message: types.Message):
    try:
        folder = message.get_args().strip()
    except AttributeError:
        parts = message.text.split(maxsplit=1)
        folder = parts[1].strip() if len(parts) > 1 else ""

    if not folder:
        return await message.answer("Укажите путь к папке: /add /MyFolder")

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user or not user.yadisk_token:
            return await message.answer("Сначала зарегистрируйтесь и сохраните токен.")
        # здесь добавить в БД TrackedFolder и оповестить подписчиков
        await message.answer(f"Папка `{folder}` теперь отслеживается.", parse_mode="Markdown")
    finally:
        db.close()

# --- /diskinfo
async def diskinfo_command(message: types.Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            return await message.answer("Сначала зарегистрируйтесь командой /start.")
        if not user.yadisk_token:
            return await message.answer("Сначала сохраните токен командой /token.")

        try:
            y = yadisk.YaDisk(token=user.yadisk_token)
            info = y.get_disk_info()
            used = info.get("used_space") or info.get("used")
            total = info.get("total_space") or info.get("total")
            if used is not None and total is not None:
                await message.answer(f"Использовано {used} из {total} байт.")
            else:
                await message.answer("Информация о диске получена.")
        except Exception:
            await message.answer("Не удалось получить информацию о диске.")
    finally:
        db.close()

# точка регистрации всех команд
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(status_command, commands=["status"])
    dp.register_message_handler(register_command, commands=["register"])
    dp.register_message_handler(token_command, commands=["token"])
    dp.register_message_handler(add_command, commands=["add"])
    dp.register_message_handler(diskinfo_command, commands=["diskinfo"])
    dp.register_message_handler(help_command, commands=["help"])