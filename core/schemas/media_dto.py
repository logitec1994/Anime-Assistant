from pydantic import BaseModel

class MediaCreate(BaseModel):
    title: str
    type: str
    total: int
    progress: int
    rating: int

class MediaOut(MediaCreate):
    id: int
    user_id: int
