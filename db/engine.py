from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DATABASE_URL = "sqlite:///db.sqlite3"  # Можно заменить на PostgreSQL/MySQL при необходимости

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Создание таблиц
Base.metadata.create_all(bind=engine)
