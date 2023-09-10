# from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# from config.database import get_db
# from config.settings import settings

from models import Chat
from schemas import MessageRequest

def get_chats(db: Session, discussion_id: str):
    return db.query(Chat).filter(Chat.discussion_id == discussion_id).all()

def create_chat(db: Session, content: str, discussion_id: str):
    db_chat = Chat(
        content = content,
        discussion_id = discussion_id,
        is_ai = False,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_ai_chat(db: Session, content: str, discussion_id: str, chat_id: str):
    db_chat = Chat(
        content = content,
        discussion_id = discussion_id,
        chat_id = chat_id,
        is_ai = True,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat