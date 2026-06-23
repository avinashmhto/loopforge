from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Shopping list"])
    content: str = Field(..., min_length=1, max_length=10000, examples=["Milk, eggs, bread"])

    @field_validator("title", "content")
    @classmethod
    def strip_and_reject_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class NoteCreate(NoteBase):
    pass


class NoteReplace(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)

    @field_validator("title", "content")
    @classmethod
    def strip_and_reject_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "NoteUpdate":
        if self.title is None and self.content is None:
            raise ValueError("At least one of title or content must be provided")
        return self


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
