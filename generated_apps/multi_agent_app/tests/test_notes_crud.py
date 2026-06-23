from .helpers import NOTES_URL, create_note, extract_notes


def test_create_note_returns_created_note_with_expected_fields(client):
    payload = {"title": "First note", "content": "This is the first note."}

    response = client.post(NOTES_URL, json=payload)

    assert response.status_code in {200, 201}, response.text
    note = response.json()
    assert note["id"] is not None
    assert note["title"] == payload["title"]
    assert note["content"] == payload["content"]
    assert "created_at" in note
    assert "updated_at" in note


def test_list_notes_returns_created_notes(client):
    first = create_note(client, title="List note A", content="Alpha")
    second = create_note(client, title="List note B", content="Beta")

    response = client.get(NOTES_URL)

    assert response.status_code == 200, response.text
    notes = extract_notes(response)
    ids = {note.get("id") for note in notes}
    assert first["id"] in ids
    assert second["id"] in ids


def test_get_note_by_id_returns_matching_note(client):
    created = create_note(client, title="Readable note", content="Read me")

    response = client.get(f"{NOTES_URL}/{created['id']}")

    assert response.status_code == 200, response.text
    note = response.json()
    assert note["id"] == created["id"]
    assert note["title"] == created["title"]
    assert note["content"] == created["content"]


def test_update_note_replaces_title_and_content(client):
    created = create_note(client, title="Old title", content="Old content")
    payload = {"title": "Updated title", "content": "Updated content"}

    response = client.put(f"{NOTES_URL}/{created['id']}", json=payload)

    assert response.status_code == 200, response.text
    updated = response.json()
    assert updated["id"] == created["id"]
    assert updated["title"] == payload["title"]
    assert updated["content"] == payload["content"]

    get_response = client.get(f"{NOTES_URL}/{created['id']}")
    assert get_response.status_code == 200, get_response.text
    persisted = get_response.json()
    assert persisted["title"] == payload["title"]
    assert persisted["content"] == payload["content"]


def test_delete_note_removes_note_from_api(client):
    created = create_note(client, title="Delete me", content="Temporary")

    delete_response = client.delete(f"{NOTES_URL}/{created['id']}")

    assert delete_response.status_code in {200, 204}, delete_response.text

    get_response = client.get(f"{NOTES_URL}/{created['id']}")
    assert get_response.status_code == 404, get_response.text

    list_response = client.get(NOTES_URL)
    assert list_response.status_code == 200, list_response.text
    notes = extract_notes(list_response)
    assert created["id"] not in {note.get("id") for note in notes}
