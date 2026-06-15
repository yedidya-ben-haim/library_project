from fastapi import APIRouter, HTTPException
from database import book_db

new_book = book_db.BookDB()

router = APIRouter()


@router.get("/books")
def get_all_books():
    return new_book.get_all_books()


@router.get("/books/{id}")
def get_book_by_id(id: int):
    book = new_book.get_book_by_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="The book does not exist.")

