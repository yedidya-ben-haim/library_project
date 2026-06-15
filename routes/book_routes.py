from fastapi import APIRouter
from database import book_db

new_book = book_db.BookDB()

router = APIRouter()


@router.get("/books")
def get_all_books():
    return new_book.get_all_books()

@router.get("/books")

