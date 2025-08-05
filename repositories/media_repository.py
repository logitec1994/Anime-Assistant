from database.db import Database
from models.media import MediaItem, MediaCategory

class MediaRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_item(self, item: MediaItem):
        with self.db.get_session() as session:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
    
    def get_all_items(self):
        with self.db.get_session() as session:
            return session.query(MediaItem).all()
