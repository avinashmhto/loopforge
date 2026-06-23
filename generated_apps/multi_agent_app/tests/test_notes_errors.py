from .helpers import NOTES_URL


MISSING_NOTE_ID = 999_999_999


def test_get_missing_note_returns_404(client):
    response = client.get(f"{NOTES_URL}/{MISSING_NOTE_ID}")

    assert response.status_code == 404, response.text
    assert "detail" in response.json()


def test_update_missing_note_returns_404(client):
    response = client.put(
        f"{NOTES_URL}/{MISSING_NOTE_ID}",
        json={"title": "Does not exist", "content": "No note should be updated"},
    )

    assert response.status_code == 404, response.text
    assert "detail" in response.json()


def test_delete_missing_note_returns_404(client):
    response = client.delete(f"{NOTES_URL}/{MISSING_NOTE_ID}")

    assert response.status_code == 404, response.text
    assert "detail" in response.json()


def test_non_integer_note_id_is_rejected(client):
    response = client.get(f"{NOTES_URL}/not-an-integer")

    assert response.status_code == 422, response.text
    assert "detail" in response.json()
