from dataclasses import dataclass, field
from app.statuses.media_status import MediaStatus
from datetime import datetime

@dataclass
class MediaItemDTO:
    id: int | None = None
    title: str = ""
    category: str = ""
    status: MediaStatus = MediaStatus.PLANNED
    created_at: datetime = field(default_factory=datetime.now)
