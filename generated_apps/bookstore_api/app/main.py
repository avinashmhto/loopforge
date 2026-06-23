from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Bookstore API")

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

books = []

@app.get("/")
def health_check():
    return {"status": "ok", "service": "bookstore-api"}

@app.post("/books")
def create_book(book: Book):
    books.append(book)
    return book

@app.get("/books")
def list_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")