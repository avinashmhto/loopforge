from dataclasses import dataclass
from datetime import datetime


@dataclass
class NoteRecord:
    """Internal representation of a note stored in memory."""

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
