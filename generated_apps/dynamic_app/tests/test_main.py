import pytest
from fastapi.testclient import TestClient

from app.main import app, _reset_for_tests


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store():
    _reset_for_tests()
    yield
    _reset_for_tests()


def create_note(title="Test note", content="Test content"):
    return client.post("/notes", json={"title": title, "content": content})


def test_root_endpoint_returns_api_info():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Notes API", "notes_url": "/notes"}


def test_list_notes_starts_empty():
    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_create_note_returns_created_note_with_id():
    response = create_note("First", "Hello")

    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "First", "content": "Hello"}


def test_create_note_allows_default_empty_content():
    response = client.post("/notes", json={"title": "No content yet"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "No content yet", "content": ""}


def test_list_notes_returns_all_notes_ordered_by_id():
    create_note("First", "A")
    create_note("Second", "B")
    create_note("Third", "C")

    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "First", "content": "A"},
        {"id": 2, "title": "Second", "content": "B"},
        {"id": 3, "title": "Third", "content": "C"},
    ]


def test_get_note_by_id():
    create_note("Readable", "Find me")

    response = client.get("/notes/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Readable", "content": "Find me"}


def test_get_missing_note_returns_404():
    response = client.get("/notes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_put_updates_entire_note():
    create_note("Old title", "Old content")

    response = client.put("/notes/1", json={"title": "New title", "content": "New content"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "New title", "content": "New content"}
    assert client.get("/notes/1").json() == {"id": 1, "title": "New title", "content": "New content"}


def test_put_missing_note_returns_404():
    response = client.put("/notes/123", json={"title": "New title", "content": "New content"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_patch_updates_only_title():
    create_note("Old title", "Keep this content")

    response = client.patch("/notes/1", json={"title": "Patched title"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Patched title", "content": "Keep this content"}


def test_patch_updates_only_content():
    create_note("Keep this title", "Old content")

    response = client.patch("/notes/1", json={"content": "Patched content"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Keep this title", "content": "Patched content"}


def test_patch_with_empty_body_leaves_note_unchanged():
    create_note("Original", "Original content")

    response = client.patch("/notes/1", json={})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Original", "content": "Original content"}


def test_patch_missing_note_returns_404():
    response = client.patch("/notes/404", json={"title": "Does not exist"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_delete_note_removes_it():
    create_note("Temporary", "Delete me")

    delete_response = client.delete("/notes/1")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert client.get("/notes/1").status_code == 404
    assert client.get("/notes").json() == []


def test_delete_missing_note_returns_404():
    response = client.delete("/notes/42")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_ids_increment_and_are_not_reused_after_delete():
    create_note("First", "A")
    client.delete("/notes/1")

    response = create_note("Second", "B")

    assert response.status_code == 201
    assert response.json() == {"id": 2, "title": "Second", "content": "B"}


def test_create_note_requires_title():
    response = client.post("/notes", json={"content": "Missing title"})

    assert response.status_code == 422


def test_create_note_rejects_empty_title():
    response = client.post("/notes", json={"title": "", "content": "Empty title"})

    assert response.status_code == 422


def test_put_rejects_empty_title():
    create_note("Valid", "Valid content")

    response = client.put("/notes/1", json={"title": "", "content": "Invalid"})

    assert response.status_code == 422


def test_patch_rejects_empty_title():
    create_note("Valid", "Valid content")

    response = client.patch("/notes/1", json={"title": ""})

    assert response.status_code == 422


def test_patch_rejects_null_fields():
    create_note("Valid", "Valid content")

    response = client.patch("/notes/1", json={"title": None})

    assert response.status_code == 422
    assert response.json()["detail"] == "Fields cannot be null"


def test_invalid_note_id_path_returns_422():
    response = client.get("/notes/not-an-int")

    assert response.status_code == 422
