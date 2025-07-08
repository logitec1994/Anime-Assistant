from repositories.media_repo import MediaRepository # Только для аннотации типов
from core.schemas.media_dto import MediaCreate # Только для аннотации типов

class MediaService:
    def __init__(self, repo: MediaRepository):
        self.repo = repo
    
    async def add_media(self, user_id: int, data: MediaCreate):
        """
        Добавляет медиа для пользователя.
        :param user_id: ID пользователя
        :param data: Данные медиа
        :return: Созданный объект UserMedia
        """
        return await self.repo.create(user_id, data)

    async def remove_media(self, user_id: int, media_id: int):
        """
        Удаляет медиа пользователя.
        :param user_id: ID пользователя
        :param media_id: ID медиа
        :return: None
        """
        await self.repo.delete(user_id, media_id)
