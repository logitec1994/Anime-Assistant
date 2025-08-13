from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = Session(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db_session():
    return SessionLocal
