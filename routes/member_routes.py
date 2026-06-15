from database import member_db, db_connection
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

manage_members = member_db.MemberDB()
router = APIRouter()

class CreateMember(BaseModel):
    name: str
    email: str


@router.post("/members", status_code=201)
def create_member(data: CreateMember):
    data = data.model_dump()
    try:
        member_created = manage_members.create_member(data)
    except KeyError:
        raise HTTPException(status_code=400, detail="The email already exists")
    if not member_created:
        raise HTTPException(status_code=400, detail="Error adding members")


@@router.get("/members")

