from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db

from models import User
from schemas import DiscussionRequest
from crud import get_discussions, get_current_user, create_discussion


app = APIRouter(
    tags=["Chats"],
    prefix="/chat"
)

@app.get("/", status_code=status.HTTP_200_OK)
def list_discussion(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    disc = get_discussions(db, current_user.id)
    return disc

@app.post("/add", status_code=status.HTTP_201_CREATED)
def add_discussion(chat: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    disc = create_discussion(db, current_user.id, chat)
    return disc