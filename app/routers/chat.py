from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_db

from crud import get_current_user, get_chats, create_ai_chat, create_chat
from models import User, Discussion, Chat
from schemas import MessageRequest

app = APIRouter(
    tags=["Messages"],
    prefix="/message"
)

@app.get("/", status_code=status.HTTP_200_OK)
def list_message(discussion_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mes = get_chats(db, discussion_id)
    return mes

@app.post("/prompt", status_code=status.HTTP_201_CREATED)
def prompt_message(discussion_id: str, message: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prompt = create_chat(db, message, discussion_id)
    return prompt

@app.post("/prompt_ai", status_code=status.HTTP_201_CREATED)
def response_message(chat_id: str, discussion_id: str, response: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = create_ai_chat(db, response, discussion_id, chat_id)
    return response 