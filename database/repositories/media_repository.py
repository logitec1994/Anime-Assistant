from database.models.media_item import MediaItemORM
from app.models.media_item import MediaItemDTO
from app.statuses.media_status import MediaStatus

class MediaRepository:
    def __init__(self, session) -> None:
        self.session = session

    def save(self, dto: MediaItemDTO) -> MediaItemDTO:
        media_exist = self.get_by_title(dto.title)
        if media_exist:
            return media_exist

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

    def save_or_update(self, dto: MediaItemDTO) -> MediaItemDTO:
        media_exist = self.get_by_title(dto.title)

        if media_exist:
            orm_item = self.session.query(MediaItemORM).get(media_exist.id)
            orm_item.title = dto.title
            orm_item.category = dto.category
            orm_item.status = dto.status.name

            dto.id = media_exist.id
        else:
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
    
    def get_by_title(self, title: str) -> None | MediaItemDTO:
        orm_item = (
            self.session.query(MediaItemORM)
            .filter(MediaItemORM.title == title)
            .first()
        )
        return MediaItemDTO(
            id=orm_item.id,
            title=orm_item.title,
            category=orm_item.category,
            status=MediaStatus[orm_item.status],
            created_at=orm_item.created_at
        ) if orm_item else None
