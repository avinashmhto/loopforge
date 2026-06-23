from app.core.database import InMemoryNoteStore
from app.models.note import NoteRecord
from app.schemas.note import NoteCreate, NotePatch, NoteUpdate


def create_note(store: InMemoryNoteStore, note_in: NoteCreate) -> NoteRecord:
    return store.create(title=note_in.title, content=note_in.content)


def list_notes(store: InMemoryNoteStore, skip: int = 0, limit: int = 100) -> list[NoteRecord]:
    return store.list(skip=skip, limit=limit)


def get_note(store: InMemoryNoteStore, note_id: int) -> NoteRecord | None:
    return store.get(note_id)


def update_note(store: InMemoryNoteStore, note_id: int, note_in: NoteUpdate) -> NoteRecord | None:
    return store.update(note_id, note_in.model_dump())


def patch_note(store: InMemoryNoteStore, note_id: int, note_in: NotePatch) -> NoteRecord | None:
    changes = note_in.model_dump(exclude_unset=True, exclude_none=True)
    return store.update(note_id, changes)


def delete_note(store: InMemoryNoteStore, note_id: int) -> bool:
    return store.delete(note_id)
