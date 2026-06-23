from fastapi import FastAPI

from app.api.routes.notes import router as notes_router
from app.core.config import settings
from app.core.database import InMemoryNoteStore


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        description="A small RESTful notes application backed by in-memory storage.",
    )

    app.state.note_store = InMemoryNoteStore()
    app.include_router(notes_router)

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
