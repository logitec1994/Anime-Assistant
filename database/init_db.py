from database.session import Base, engine
from database.models import Item

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
