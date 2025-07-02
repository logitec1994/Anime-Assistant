# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from shared.config import DB_PATH
from loguru import logger

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
