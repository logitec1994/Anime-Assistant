# db/models.py
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import enum

# Базовый класс для объявления моделей
Base = declarative_base()

# Перечисление для статуса аниме в списке пользователя
class AnimeStatus(enum.Enum):
    TO_WATCH = "to_watch"      # Нужно посмотреть
    WATCHING = "watching"      # Смотрю сейчас
    WATCHED = "watched"        # Просмотрено
    REWATCH = "rewatch"        # Нужно пересмотреть

# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с таблицей UserAnime
    user_anime = relationship("UserAnime", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"

# Модель аниме (справочник)
class Anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False) # Название аниме
    mal_id = Column(Integer, unique=True, nullable=True) # ID на MyAnimeList, если есть
    total_episodes = Column(Integer, nullable=True) # Общее количество эпизодов

    # Связь с таблицей UserAnime
    user_anime = relationship("UserAnime", back_populates="anime", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Anime(id={self.id}, title='{self.title}')>"

# Модель для связи пользователя с аниме и его статусом
class UserAnime(Base):
    __tablename__ = 'user_anime'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
    status = Column(Enum(AnimeStatus), nullable=False)
    current_episode = Column(Integer, default=0) # Текущая серия (для статуса WATCHING)
    watched_time_in_sec = Column(Integer, default=0) # Время просмотра в секундах для текущей серии
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи с таблицами User и Anime
    user = relationship("User", back_populates="user_anime")
    anime = relationship("Anime", back_populates="user_anime")

    def __repr__(self):
        return (f"<UserAnime(user_id={self.user_id}, anime_id={self.anime_id}, "
                f"status='{self.status.value}', current_episode={self.current_episode})>")
