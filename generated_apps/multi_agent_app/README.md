# Notes API

A FastAPI notes application with RESTful CRUD endpoints and in-memory storage.

## Features

- Create, list, retrieve, replace, partially update, and delete notes
- Validates required fields, blank text, invalid IDs, and incorrect types
- Uses proper HTTP status codes
- Stores notes in process-local memory only

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| POST | `/notes` | Create a note |
| GET | `/notes` | List notes |
| GET | `/notes/{note_id}` | Retrieve a note |
| PUT | `/notes/{note_id}` | Replace a note |
| PATCH | `/notes/{note_id}` | Partially update a note |
| DELETE | `/notes/{note_id}` | Delete a note |

## Example requests

Create a note:

```bash
curl -X POST http://127.0.0.1:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"First note","content":"Remember to test the API"}'
```

List notes:

```bash
curl http://127.0.0.1:8000/notes
```

Patch a note:

```bash
curl -X PATCH http://127.0.0.1:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"content":"Updated content"}'
```

Delete a note:

```bash
curl -X DELETE http://127.0.0.1:8000/notes/1
```

## Storage note

This implementation uses in-memory storage only. Notes are not persisted across process restarts.
