from database import member_db, db_connection
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

manage_members = member_db.MemberDB()
router = APIRouter()

class CreateMember(BaseModel):
    name: str
    email: str

class UpdateMember(BaseModel):
    name: str | None = None
    email: str | None = None


@router.post("/members", status_code=201)
def create_member(data: CreateMember):
    data = data.model_dump()
    try:
        member_created = manage_members.create_member(data)
    except KeyError:
        raise HTTPException(status_code=400, detail="The email already exists")
    if not member_created:
        raise HTTPException(status_code=400, detail="Error adding members")


@router.get("/members")
def all_members():
    return manage_members.get_all_members()

@router.get("/members/{id}")
def get_member_by_id(id: int):
    book = manage_members.get_member_by_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Member not found")

@router.put("/members/{id}")
def update_member(id: int, data: UpdateMember):
    data = data.model_dump(exclude_unset=True)

    try:
        is_update = manage_members.update_member(id, data)
    except KeyError:
        raise HTTPException(status_code=400, detail="Unable to update member")

    return is_update

@router.put("/members/{id}/deactivate")
def deactivate_member(id: int):
    try:
        is_update = manage_members.deactivate_member(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Member not found")

    return is_update

@router.put("/members/{id}/activate")
def activate_member(id: int):
    try:
        is_update = manage_members.activate_member(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Member not found")

    return is_update