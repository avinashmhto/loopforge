from __future__ import annotations

from threading import RLock

from app.models import Note, utc_now


class NotesRepository:
    """Thread-safe in-memory repository for notes.

    Data is intentionally not persisted across process restarts. The repository
    exposes a clear method to make test isolation straightforward when needed.
    """

    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id = 1
        self._lock = RLock()

    def list_notes(self) -> list[Note]:
        with self._lock:
            return sorted(self._notes.values(), key=lambda note: note.id)

    def get_note(self, note_id: int) -> Note | None:
        with self._lock:
            return self._notes.get(note_id)

    def create_note(self, title: str, content: str) -> Note:
        with self._lock:
            now = utc_now()
            note = Note(
                id=self._next_id,
                title=title,
                content=content,
                created_at=now,
                updated_at=now,
            )
            self._notes[note.id] = note
            self._next_id += 1
            return note

    def replace_note(self, note_id: int, title: str, content: str) -> Note | None:
        with self._lock:
            note = self._notes.get(note_id)
            if note is None:
                return None
            note.title = title
            note.content = content
            note.updated_at = utc_now()
            return note

    def update_note(
        self,
        note_id: int,
        *,
        title: str | None = None,
        content: str | None = None,
    ) -> Note | None:
        with self._lock:
            note = self._notes.get(note_id)
            if note is None:
                return None
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            note.updated_at = utc_now()
            return note

    def delete_note(self, note_id: int) -> bool:
        with self._lock:
            if note_id not in self._notes:
                return False
            del self._notes[note_id]
            return True

    def clear(self) -> None:
        with self._lock:
            self._notes.clear()
            self._next_id = 1
