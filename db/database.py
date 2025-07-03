from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
import enum
from sqlalchemy.exc import IntegrityError
from loguru import logger
from shared.config import DB_PATH
from db.models import Base, User, Anime, UserAnime, AnimeStatus


class Database:
    def __init__(self, db_url=f"sqlite:///{DB_PATH}"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Database engine initialized for {db_url}")

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created or already exist.")

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_user_by_telegram_id(self, telegram_id: int):
        with self.SessionLocal() as session:
            return session.query(User).filter_by(telegram_id=telegram_id).first()
    
    def get_anime_by_title(self, title: str):
        with self.SessionLocal() as session:
            return session.query(Anime).filter_by(title=title).first()
    
    def create_anime(self, title: str, mal_id: int = None, total_episodes: int = None):
        with self.SessionLocal() as session:
            anime = self.get_anime_by_title(title)
            if anime:
                logger.info(f"Anime {title} already exists in the database")
                return anime
            new_anime = Anime(title=title, mal_id=mal_id, total_episodes=total_episodes)
            try:
                session.add(new_anime)
                session.commit()
                session.refresh(new_anime)
                logger.info(f"Anime {title} added to the anime list")
                return new_anime
            except IntegrityError:
                session.rollback()
                logger.warning(f"Anime {title} already exists in the database")
                return self.get_anime_by_title(title)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating anime {title}: {e}")
                raise

    def add_user_anime(self, user_id: int, anime_id: int, status: AnimeStatus, current_episode: int = 0, watched_time_in_sec: int = 0):
        with self.SessionLocal() as session:
            user_anime_entry = session.query(UserAnime).filter_by(user_id=user_id, anime_id=anime_id).first()

            if user_anime_entry:
                user_anime_entry.status = status
                user_anime_entry.current_episode = current_episode
                user_anime_entry.watched_time_in_sec = watched_time_in_sec
                logger.info(f"Updated UserAnime entry for user {user_id} and anime {anime_id}")
            else:
                user_anime_entry = UserAnime(
                    user_id=user_id,
                    anime_id=anime_id,
                    status=status,
                    current_episode=current_episode,
                    watched_time_in_sec=watched_time_in_sec
                )
                session.add(user_anime_entry)
                logger.info(f"Added UserAnime entry for user {user_id} and anime {anime_id}")
            
            try:
                session.commit()
                session.refresh(user_anime_entry)
                return user_anime_entry
            except Exception as e:
                session.rollback()
                logger.error(f"Error adding/updating UserAnime entry: {e}")
                raise

    def get_user_anime_list(self, user_id: int, status: AnimeStatus = None, offset: int = 0, limit: int = 100):
        with self.SessionLocal() as session:
            query = session.query(UserAnime).filter(UserAnime.user_id == user_id)

            if status:
                query = query.filter(UserAnime.status == status)
            
            total_count = query.count()
            user_anime_entries = query.order_by(UserAnime.added_at.desc()).offset(offset).limit(limit).all()
            for entry in user_anime_entries:
                entry.anime
            
            return user_anime_entries, total_count
    
    def get_user_anime_entry(self, user_anime_id: int, new_status: AnimeStatus = None, current_episode: int = None, watched_time_in_sec: int = None):
        with self.SessionLocal() as session:
            entry = session.query(UserAnime).filter_by(id=user_anime_id).first()
            if not entry:
                logger.warning(f"UserAnime entry with ID {user_anime_id} not found")
                return None
            
            updated = False
            if new_status is not None and entry.status != new_status:
                entry.status = new_status
                updated = True
            if current_episode is not None and entry.current_episode != current_episode:
                entry.current_episode = current_episode
                updated = True
            if watched_time_in_sec is not None and entry.watched_time_in_sec != watched_time_in_sec:
                entry.watched_time_in_sec = watched_time_in_sec
                updated = True
            
            if updated:
                try:
                    session.commit()
                    session.refresh(entry)
                    logger.info(f"Updated UserAnime entry {user_anime_id}")
                    return entry
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error updating UserAnime entry {user_anime_id}: {e}")
                    raise
            else:
                logger.info(f"No updates made to UserAnime entry {user_anime_id}")
                return entry

    def delete_user_anime_entry(self, user_anime_id: int):
        with self.SessionLocal() as session:
            entry = session.query(UserAnime).filter_by(id=user_anime_id).first()
            if entry:
                session.delete(entry)
                try:
                    session.commit()
                    logger.info(f"Deleted UserAnime entry {user_anime_id}")
                    return True
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error deleting UserAnime entry {user_anime_id}: {e}")
                    raise
            else:
                logger.warning(f"UserAnime entry with ID {user_anime_id} not found")
                return False
