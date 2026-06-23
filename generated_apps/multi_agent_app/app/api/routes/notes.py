from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status

from app.api.deps import get_note_store
from app.core.database import InMemoryNoteStore
from app.crud.notes import create_note, delete_note, get_note, list_notes, patch_note, update_note
from app.models.note import NoteRecord
from app.schemas.note import NoteCreate, NotePatch, NoteRead, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

NoteId = Annotated[int, Path(ge=1, description="Positive integer note ID")]
StoreDep = Annotated[InMemoryNoteStore, Depends(get_note_store)]


def _note_or_404(note: NoteRecord | None) -> NoteRecord:
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note_endpoint(payload: NoteCreate, store: StoreDep) -> NoteRecord:
    return create_note(store, payload)


@router.get("", response_model=list[NoteRead])
def list_notes_endpoint(
    store: StoreDep,
    skip: Annotated[int, Query(ge=0, description="Number of notes to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=1000, description="Maximum notes to return")] = 100,
) -> list[NoteRecord]:
    return list_notes(store, skip=skip, limit=limit)


@router.get("/{note_id}", response_model=NoteRead)
def retrieve_note_endpoint(note_id: NoteId, store: StoreDep) -> NoteRecord:
    return _note_or_404(get_note(store, note_id))


@router.put("/{note_id}", response_model=NoteRead)
def replace_note_endpoint(note_id: NoteId, payload: NoteUpdate, store: StoreDep) -> NoteRecord:
    return _note_or_404(update_note(store, note_id, payload))


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note_endpoint(note_id: NoteId, payload: NotePatch, store: StoreDep) -> NoteRecord:
    return _note_or_404(patch_note(store, note_id, payload))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(note_id: NoteId, store: StoreDep) -> Response:
    deleted = delete_note(store, note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
