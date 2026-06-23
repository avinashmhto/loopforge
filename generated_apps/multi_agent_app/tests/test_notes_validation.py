import pytest

from .helpers import NOTES_URL, create_note


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "Only title"},
        {"content": "Only content"},
        {"title": "", "content": "Valid content"},
        {"title": "   ", "content": "Valid content"},
        {"title": "Valid title", "content": ""},
        {"title": "Valid title", "content": "   "},
        {"title": [], "content": "Valid content"},
        {"title": "Valid title", "content": {}},
    ],
)
def test_create_note_rejects_invalid_payloads(client, payload):
    response = client.post(NOTES_URL, json=payload)

    assert response.status_code == 422, response.text
    body = response.json()
    assert "detail" in body


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"content": ""},
        {"title": "", "content": "Valid content"},
        {"title": "Valid title", "content": ""},
        {"title": [], "content": "Valid content"},
        {"title": "Valid title", "content": []},
    ],
)
def test_update_note_rejects_invalid_payloads(client, payload):
    created = create_note(client, title="Original", content="Original content")

    response = client.put(f"{NOTES_URL}/{created['id']}", json=payload)

    assert response.status_code == 422, response.text
    body = response.json()
    assert "detail" in body
