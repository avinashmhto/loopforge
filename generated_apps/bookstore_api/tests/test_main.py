from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_book():
    payload = {
        "id": 1,
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "price": 29.99
    }

    response = client.post("/books", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Clean Architecture"

def test_list_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_missing_book():
    response = client.get("/books/999")
    assert response.status_code == 404