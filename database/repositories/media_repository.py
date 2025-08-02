from database.models.media_item import MediaItemORM
from app.models.media_item import MediaItemDTO
from app.statuses.media_status import MediaStatus

class MediaRepository:
    def __init__(self, session) -> None:
        self.session = session

    def save(self, dto: MediaItemDTO) -> MediaItemDTO:
        orm_item = MediaItemORM(
            title=dto.title,
            category=dto.category,
            status=dto.status.name,
            created_at=dto.created_at
        )
        self.session.add(orm_item)
        self.session.commit()

        dto.id = orm_item.id
        return dto
    
    def get_all(self) -> list[MediaItemDTO]:
        orm_items = self.session.query(MediaItemORM).all()
        return [
            MediaItemDTO(
                id=item.id,
                title=item.title,
                category=item.category,
                status=MediaStatus[item.status],
                created_at=item.created_at
            )
            for item in orm_items
        ]
