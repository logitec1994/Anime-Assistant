from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.media import Base

class Database:
    def __init__(self, db_name: str = "sqlite:///media.db"):
        self.engine = create_engine(db_name, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def cleare_table(self):
        with self.get_session() as session:
            session.query(Base.metadata.tables['media_items']).delete()
            session.commit()

    def recreate_table(self):
        Base.metadata.drop_all(self.engine, tables=[Base.metadata.tables['media_items']])
        Base.metadata.create_all(self.engine, tables=[Base.metadata.tables['media_items']])
