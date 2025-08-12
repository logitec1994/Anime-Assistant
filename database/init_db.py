from database.session import Base
from database.models import Item
from sqlalchemy import create_engine

def init_db():
    engine = create_engine("sqlite:///anime_list.db", echo=True)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
