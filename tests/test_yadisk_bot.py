import pytest
from aiogram.types import Message, User as AiogramUser
from db.models import User, TrackedFolder, Base
from db.engine import engine, SessionLocal
from handlers.bot_commands import start_command, status_command, token_command

@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def fake_message():
    class FakeFrom:
        id = 123456

    class FakeMessage:
        from_user = FakeFrom()
        text = "/start"
        def __init__(self):
            self.responses = []
        async def answer(self, text):
            self.responses.append(text)
    return FakeMessage()

def test_start_registers_user(db, fake_message):
    # До вызова /start пользователь не существует
    assert db.query(User).count() == 0

    import asyncio
    asyncio.run(start_command(fake_message))

    # После вызова /start пользователь зарегистрирован
    user = db.query(User).filter_by(telegram_id=123456).first()
    assert user is not None
    assert "зарегистрированы" in fake_message.responses[-1]

def test_status_unregistered(fake_message):
    import asyncio
    fake_message.text = "/status"
    fake_message.from_user.id = 999999  # Нет в базе
    asyncio.run(status_command(fake_message))
    assert "не зарегистрированы" in fake_message.responses[-1].lower()

def test_token_invalid_token(db, fake_message):
    import asyncio
    db.add(User(telegram_id=123456))
    db.commit()
    fake_message.text = "/token fake_token"
    asyncio.run(token_command(fake_message))
    assert "недействительный токен" in fake_message.responses[-1].lower()
