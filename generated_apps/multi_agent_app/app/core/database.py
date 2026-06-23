from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from threading import RLock

from app.models.note import NoteRecord


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class InMemoryNoteStore:
    """Thread-safe in-memory note storage.

    This store is intentionally process-local and ephemeral. Data is lost when
    the application process restarts.
    """

    def __init__(self) -> None:
        self._notes: dict[int, NoteRecord] = {}
        self._next_id = 1
        self._lock = RLock()

    def create(self, title: str, content: str) -> NoteRecord:
        with self._lock:
            now = utc_now()
            note = NoteRecord(
                id=self._next_id,
                title=title,
                content=content,
                created_at=now,
                updated_at=now,
            )
            self._notes[note.id] = note
            self._next_id += 1
            return self._copy(note)

    def list(self, skip: int = 0, limit: int = 100) -> list[NoteRecord]:
        with self._lock:
            ordered_notes = sorted(self._notes.values(), key=lambda note: note.id)
            return [self._copy(note) for note in ordered_notes[skip : skip + limit]]

    def get(self, note_id: int) -> NoteRecord | None:
        with self._lock:
            note = self._notes.get(note_id)
            return self._copy(note) if note is not None else None

    def update(self, note_id: int, changes: dict[str, str]) -> NoteRecord | None:
        with self._lock:
            note = self._notes.get(note_id)
            if note is None:
                return None

            if "title" in changes:
                note.title = changes["title"]
            if "content" in changes:
                note.content = changes["content"]

            new_updated_at = utc_now()
            if new_updated_at <= note.updated_at:
                new_updated_at = note.updated_at + timedelta(microseconds=1)
            note.updated_at = new_updated_at

            return self._copy(note)

    def delete(self, note_id: int) -> bool:
        with self._lock:
            if note_id not in self._notes:
                return False
            del self._notes[note_id]
            return True

    def clear(self) -> None:
        """Clear all notes and reset ID generation.

        Useful for application lifecycle management and external test fixtures.
        """
        with self._lock:
            self._notes.clear()
            self._next_id = 1

    @staticmethod
    def _copy(note: NoteRecord) -> NoteRecord:
        return replace(note)
