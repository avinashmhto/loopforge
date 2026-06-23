import time

from .helpers import NOTES_URL, create_note, extract_notes, parse_datetime


def test_created_note_persists_across_multiple_requests(client):
    created = create_note(client, title="Persistent note", content="Stored content")

    first_get = client.get(f"{NOTES_URL}/{created['id']}")
    second_get = client.get(f"{NOTES_URL}/{created['id']}")
    list_response = client.get(NOTES_URL)

    assert first_get.status_code == 200, first_get.text
    assert second_get.status_code == 200, second_get.text
    assert list_response.status_code == 200, list_response.text

    assert first_get.json() == second_get.json()
    listed_ids = {note.get("id") for note in extract_notes(list_response)}
    assert created["id"] in listed_ids


def test_update_preserves_created_at_and_changes_updated_at(client):
    created = create_note(client, title="Timestamp note", content="Before update")
    assert created.get("created_at")
    assert created.get("updated_at")

    original_created_at = created["created_at"]
    original_updated_at = created["updated_at"]

    # Give implementations with second-level timestamp precision enough time to change updated_at.
    time.sleep(1.1)

    response = client.put(
        f"{NOTES_URL}/{created['id']}",
        json={"title": "Timestamp note updated", "content": "After update"},
    )

    assert response.status_code == 200, response.text
    updated = response.json()
    assert updated["id"] == created["id"]
    assert updated["created_at"] == original_created_at
    assert updated["updated_at"] != original_updated_at

    created_at = parse_datetime(updated["created_at"])
    updated_at = parse_datetime(updated["updated_at"])
    assert updated_at >= created_at


def test_deleted_note_remains_deleted_across_requests(client):
    created = create_note(client, title="Gone note", content="Delete persistence")

    delete_response = client.delete(f"{NOTES_URL}/{created['id']}")
    assert delete_response.status_code in {200, 204}, delete_response.text

    for _ in range(2):
        get_response = client.get(f"{NOTES_URL}/{created['id']}")
        assert get_response.status_code == 404, get_response.text

    list_response = client.get(NOTES_URL)
    assert list_response.status_code == 200, list_response.text
    assert created["id"] not in {note.get("id") for note in extract_notes(list_response)}
