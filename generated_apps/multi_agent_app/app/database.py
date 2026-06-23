from app.crud import NotesRepository


notes_repository = NotesRepository()


def get_notes_repository() -> NotesRepository:
    """FastAPI dependency returning the application-wide in-memory repository."""
    return notes_repository
