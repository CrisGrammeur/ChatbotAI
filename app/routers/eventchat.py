from fastapi import APIRouter, status, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
# from sqlalchemy import Date
from config.database import get_db
import json

from crud import get_current_user, get_chats, create_chat, like_chat
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
def prompt_message(discussion_id: str, message: str, answer: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # url='http://127.0.0.1:8001/chatbot'

    # data1 = {
    #     "collect_name": "entouragetest10",
    #     "query": message,
    #     "json_data": json_data,
    #     "model": "gpt-4",
    #     "temp": 0.3,
    #     "templa": "As a career development expert, you need to provide a helpful and professional response to the user's question or problem. Add to your answers interesting professional profiles related to his question. Remember that you should never invent or provide professional profiles that are not in the CONTEXT provided."
    # }
    # prompt = requests.post(url, params=data1)
    
    # if prompt.status_code == 200:
    #     result = prompt.json()
    #     bot_response = result["bot_response"]
    #     answer = bot_response["answer"]
    #     print("###############################", answer, str(message))

    #     response = str(answer)

        return create_chat(db, message, answer, discussion_id)
    # else:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# @app.post("/prompt_ai", status_code=status.HTTP_201_CREATED)
# def response_message(chat_id: str, discussion_id: str, response: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     response = create_ai_chat(db, response, discussion_id, chat_id)
#     return response

@app.put("/like", status_code=status.HTTP_200_OK)
def like_message(chat_id: str, liked: bool = True, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = like_chat(db, chat_id, liked)
    return like