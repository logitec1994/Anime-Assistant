from database.db import Database
from models.media import MediaItem, MediaStatus

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

    def get_item_by_id(self, item_id: int) -> MediaItem:
        with self.db.get_session() as session:
            return session.query(MediaItem).filter(MediaItem.id == item_id).first()
    
    def update_status(self, item_id: int, new_status: MediaStatus) -> MediaItem:
        with self.db.get_session() as session:
            item = session.query(MediaItem).filter(MediaItem.id == item_id).first()
            if item:
                item.status = new_status
                session.commit()
                session.refresh(item)
                return item
            return None
