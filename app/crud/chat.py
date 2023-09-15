from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
# from sqlalchemy import Date
# from config.database import get_db
# from config.settings import settings

from models import Chat
from schemas import MessageRequest

def get_chats(db: Session, discussion_id: str):
    # if filter is None:
    return db.query(Chat).filter(Chat.discussion_id == discussion_id).all()
    # else:
    #     return db.query(Chat).filter(Chat.discussion_id == discussion_id, Chat.send_at == date).all()

def create_chat(db: Session, query: str, response: str, discussion_id: str):
    db_chat = Chat(
        query = query,
        response = response,
        discussion_id = discussion_id,
        send_at = date.today()
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# def create_ai_chat(db: Session, content: str, discussion_id: str):
#     db_chat = Chat(
#         content = content,
#         discussion_id = discussion_id,
#         # chat_id = chat_id,
#         is_ai = True,
#         is_liked = None
#     )
#     db.add(db_chat)
#     db.commit()
#     db.refresh(db_chat)
#     return db_chat

def like_chat(db: Session, chat_id: str, liked: bool):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if liked:
        db.query(Chat).filter(Chat.chat_id == chat_id).update({
            'is_liked': True
        })
    db.query(Chat).filter(Chat.chat_id == chat_id).update({
        'is_liked': False
    })
    db.commit()
    db.refresh(db_chat)
    return db_chat
    