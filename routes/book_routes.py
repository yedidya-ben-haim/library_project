import uvicorn
from fastapi import APIRouter, HTTPException
from database import book_db, member_db
from pydantic import BaseModel
from typing import Literal


mang_book = book_db.BookDB()
mang_member = member_db.MemberDB()
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
    return mang_book.get_all_books()


@router.get("/books/{id}")
def get_book_by_id(id: int):
    book = mang_book.get_book_by_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/books", status_code=201)
def create_book(data: CreateBook):
    data = data.model_dump()
    book_created = mang_book.create_book(data)
    if not book_created:
        raise HTTPException(status_code=400, detail="The book was not created.")

@router.put("/books/{id}")
def update_book(id: int,data: UpdateBook):
    data = data.model_dump(exclude_unset=True)
    print(data)
    if data:
        try:
            mang_book.update_book(id, data)
        except KeyError:
            raise HTTPException(status_code=404, detail="The book does not exist")
    else:
        raise HTTPException(status_code=400, detail="The book has not been updated")

@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    book_to_borrow = mang_book.get_book_by_id(id)
    borrow_member = mang_member.get_member_by_id(member_id)

    # chack if id and member_id exists
    if not book_to_borrow or not borrow_member:
        raise HTTPException(status_code=404, detail="The member ID or book does not exist")
    if not borrow_member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is not active")
    if book_to_borrow["is_available"] == 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    if mang_book.count_active_borrows_by_member(member_id) >= 3:
        raise HTTPException(status_code=400, detail="Member has reached maximum borrows")

    mang_book.set_available(id,0, member_id)
    mang_member.increment_borrows(member_id)

@router.put("/books/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    book_to_return= mang_book.get_book_by_id(id)
    return_member = mang_member.get_member_by_id(member_id)

    # chack if id and member_id exists
    if not book_to_return or not return_member:
        raise HTTPException(status_code=404, detail="The member ID or book does not exist")
    if not return_member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is not active")

    mang_book.set_available(id, 1, None)

