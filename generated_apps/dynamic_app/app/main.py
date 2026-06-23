from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


app = FastAPI(title="Notes API", version="1.0.0")


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(default="", max_length=5000)


class NoteUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(default="", max_length=5000)


class NotePatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, max_length=5000)


class NoteOut(BaseModel):
    id: int
    title: str
    content: str


_notes: Dict[int, dict] = {}
_next_id = 1


def _model_to_dict(model: BaseModel, **kwargs) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump(**kwargs)
    return model.dict(**kwargs)


def _reset_for_tests() -> None:
    global _next_id
    _notes.clear()
    _next_id = 1


@app.get("/")
def root() -> dict:
    return {"message": "Notes API", "notes_url": "/notes"}


@app.get("/notes", response_model=List[NoteOut])
def list_notes() -> List[dict]:
    return [_notes[note_id] for note_id in sorted(_notes)]


@app.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> dict:
    global _next_id
    note_data = _model_to_dict(note)
    stored_note = {"id": _next_id, "title": note_data["title"], "content": note_data["content"]}
    _notes[_next_id] = stored_note
    _next_id += 1
    return stored_note


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int) -> dict:
    if note_id not in _notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return _notes[note_id]


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteUpdate) -> dict:
    if note_id not in _notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note_data = _model_to_dict(note)
    _notes[note_id] = {"id": note_id, "title": note_data["title"], "content": note_data["content"]}
    return _notes[note_id]


@app.patch("/notes/{note_id}", response_model=NoteOut)
def patch_note(note_id: int, note: NotePatch) -> dict:
    if note_id not in _notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updates = _model_to_dict(note, exclude_unset=True)
    if any(value is None for value in updates.values()):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fields cannot be null")

    _notes[note_id].update(updates)
    return _notes[note_id]


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int) -> Response:
    if note_id not in _notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    del _notes[note_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
