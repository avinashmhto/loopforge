from fastapi import Request

from app.core.database import InMemoryNoteStore


def get_note_store(request: Request) -> InMemoryNoteStore:
    """Return the application's in-memory note store."""
    return request.app.state.note_store
