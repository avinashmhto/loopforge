from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings.

    The app intentionally uses in-memory storage only, so no database URL or
    external persistence configuration is required.
    """

    project_name: str = "Notes API"
    version: str = "1.0.0"


settings = Settings()
