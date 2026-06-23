from dataclasses import dataclass
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Note:
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
