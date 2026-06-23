from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator, model_validator


class _TextValidationMixin:
    @classmethod
    def _clean_text(cls, value: object, field_name: str) -> object:
        if value is None:
            raise ValueError(f"{field_name} cannot be null")
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                raise ValueError(f"{field_name} cannot be empty")
            return cleaned
        return value


class NoteBase(_TextValidationMixin, BaseModel):
    title: StrictStr = Field(..., min_length=1, max_length=200, description="Note title")
    content: StrictStr = Field(..., min_length=1, max_length=10000, description="Note content")

    @field_validator("title", "content", mode="before")
    @classmethod
    def validate_non_empty_text(cls, value: object, info):
        return cls._clean_text(value, info.field_name)


class NoteCreate(NoteBase):
    """Payload for creating a note."""


class NoteUpdate(NoteBase):
    """Payload for replacing a note with complete data."""


class NotePatch(_TextValidationMixin, BaseModel):
    """Payload for partially updating a note.

    At least one supported field must be provided.
    """

    title: StrictStr | None = Field(default=None, min_length=1, max_length=200)
    content: StrictStr | None = Field(default=None, min_length=1, max_length=10000)

    @field_validator("title", "content", mode="before")
    @classmethod
    def validate_optional_non_empty_text(cls, value: object, info):
        return cls._clean_text(value, info.field_name)

    @model_validator(mode="after")
    def require_at_least_one_field(self):
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
