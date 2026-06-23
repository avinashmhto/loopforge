from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import Response

from app.crud import NotesRepository
from app.database import get_notes_repository
from app.schemas import NoteCreate, NoteRead, NoteReplace, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: NoteCreate,
    repository: NotesRepository = Depends(get_notes_repository),
) -> NoteRead:
    return repository.create_note(title=payload.title, content=payload.content)


@router.get("", response_model=list[NoteRead], status_code=status.HTTP_200_OK)
def list_notes(
    repository: NotesRepository = Depends(get_notes_repository),
) -> list[NoteRead]:
    return repository.list_notes()


@router.get("/{note_id}", response_model=NoteRead, status_code=status.HTTP_200_OK)
def retrieve_note(
    note_id: int = Path(..., ge=1),
    repository: NotesRepository = Depends(get_notes_repository),
) -> NoteRead:
    note = repository.get_note(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} was not found",
        )
    return note


@router.put("/{note_id}", response_model=NoteRead, status_code=status.HTTP_200_OK)
def replace_note(
    payload: NoteReplace,
    note_id: int = Path(..., ge=1),
    repository: NotesRepository = Depends(get_notes_repository),
) -> NoteRead:
    note = repository.replace_note(
        note_id=note_id,
        title=payload.title,
        content=payload.content,
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} was not found",
        )
    return note


@router.patch("/{note_id}", response_model=NoteRead, status_code=status.HTTP_200_OK)
def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1),
    repository: NotesRepository = Depends(get_notes_repository),
) -> NoteRead:
    update_data = payload.model_dump(exclude_unset=True)
    note = repository.update_note(note_id=note_id, **update_data)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} was not found",
        )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int = Path(..., ge=1),
    repository: NotesRepository = Depends(get_notes_repository),
) -> Response:
    deleted = repository.delete_note(note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
