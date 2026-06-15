from fastapi import APIRouter, HTTPException
from database import book_db
from pydantic import BaseModel
from typing import Literal

new_book = book_db.BookDB()
router = APIRouter()


class CreateBook(BaseModel):
    title: str
    author: str
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]

@router.get("/books")
def get_all_books():
    return new_book.get_all_books()


@router.get("/books/{id}")
def get_book_by_id(id: int):
    book = new_book.get_book_by_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post("/books", status_code=201)
def create_book(data: CreateBook):
    data = data.model_dump()
    book_created = new_book.create_book(data)
    if not book_created:
        raise HTTPException(status_code=400, detail="The book was not created.")

