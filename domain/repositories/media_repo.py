from core.models.user_media import UserMedia
from core.schemas.media_dto import MediaCreate # Только для аннотации типов

class MediaRepository:
    def __init__(self, session):
        self.session = session
    
    async def create(self, user_id: int, data: MediaCreate) -> UserMedia:
        media = UserMedia(**data.model_dump(), user_id=user_id)
        self.session.add(media)
        await self.session.commit()
        return media

    async def delete(self, user_id: int, media_id: int) -> None:
        media = await self.session.get(UserMedia, media_id)
        if media and media.user_id == user_id:
            await self.session.delete(media)
            await self.session.commit()
