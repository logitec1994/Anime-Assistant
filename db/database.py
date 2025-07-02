# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, User, Anime, UserAnime, AnimeStatus
from shared.config import DB_PATH
from loguru import logger
from sqlalchemy.exc import IntegrityError

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
