from datetime import datetime


NOTES_URL = "/notes"


def extract_notes(response_or_data):
    """Return a list of notes from a list response or a common envelope shape."""
    data = response_or_data.json() if hasattr(response_or_data, "json") else response_or_data

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("items", "notes", "data", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return value

    raise AssertionError(f"Could not extract notes list from response payload: {data!r}")


def create_note(client, title="Test note", content="Test note content"):
    response = client.post(NOTES_URL, json={"title": title, "content": content})
    assert response.status_code in {200, 201}, response.text

    note = response.json()
    assert isinstance(note, dict), note
    assert note.get("id") is not None, note
    assert note.get("title") == title
    assert note.get("content") == content
    return note


def clear_notes(client):
    """Best-effort cleanup for apps backed by in-memory or persistent storage."""
    response = client.get(NOTES_URL)
    if response.status_code != 200:
        return

    try:
        notes = extract_notes(response)
    except AssertionError:
        return

    for note in notes:
        if isinstance(note, dict) and note.get("id") is not None:
            client.delete(f"{NOTES_URL}/{note['id']}")


def parse_datetime(value):
    assert value, "Expected a non-empty datetime value"
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
