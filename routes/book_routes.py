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

class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"] | None = None
    is_available: bool | None = None
    borrowed_by_member_id: int | None = None


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

@router.put("/books/{id}")
def update_book(id: int,data: UpdateBook):
    data = data.model_dump(exclude_unset=True)
    print(data)
    if data:
        try:
            new_book.update_book(id, data)
        except KeyError:
            raise HTTPException(status_code=404, detail="The book does not exist")
    else:
        HTTPException(status_code=400, detail="The book has not been updated")