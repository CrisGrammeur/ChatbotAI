from fastapi import APIRouter, status, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
# from sqlalchemy import Date
from config.database import get_db
import json
from typing import List
import datetime
from crud import get_current_user, get_chats, create_chat, like_chat
from models import User, Converse, eventConverse
from schemas import MessageRequest
import pandas as pd
from fastapi.responses import StreamingResponse # Add to Top
from fastapi.responses import FileResponse
import io
from tempfile import NamedTemporaryFile
import csv
app = APIRouter(
    tags=["Dashboard"],
    prefix="/dashboard"
)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

@app.get("/userstats", status_code=status.HTTP_200_OK)
def count_user( db: Session = Depends(get_db)):
    count = db.query(User).count()
    users = db.query(User).all()
    today_users = db.query(User).filter_by(created_at = today).all()
    today_users_count = db.query(User).filter_by(created_at = today).count()
    yesterday_users_count = db.query(User).filter_by(created_at = yesterday).count()
    usr = users.reverse()
    return {
            "user_list": users,
            "count": count,
            "today_users": today_users,
            "today_users_count":today_users_count,
            "yesterday_users_count": yesterday_users_count
            }



@app.get("/conversestats", status_code=status.HTTP_200_OK)
def count_converse(db: Session = Depends(get_db)):
    converses = db.query(Converse).all()
    count_converse = db.query(Converse).count()
    liked_converse = db.query(Converse).filter_by(isliked = True).all()
    liked_converse_count = db.query(Converse).filter_by(isliked = True).count()
    disliked_converse = db.query(Converse).filter_by(isliked = False).all()
    disliked_converse_count = db.query(Converse).filter_by(isliked = False).count()

    # query = len(db.query(User).all())
    con = converses.reverse()
    return {"converses":converses,"count_converse":count_converse, "liked_converse":liked_converse,"liked_converse_count":liked_converse_count,"disliked_converse":disliked_converse, "disliked_converse_count":disliked_converse_count   }


@app.get("/eventconversestats", status_code=status.HTTP_200_OK)
def count_converse(db: Session = Depends(get_db)):
    converses = db.query(eventConverse).all()
    count_converse = db.query(eventConverse).count()
    liked_converse = db.query(eventConverse).filter_by(isliked = True).all()
    liked_converse_count = db.query(eventConverse).filter_by(isliked = True).count()
    disliked_converse = db.query(eventConverse).filter_by(isliked = False).all()
    disliked_converse_count = db.query(eventConverse).filter_by(isliked = False).count()

    # query = len(db.query(User).all())
    con = converses.reverse()
    return {"converses":converses,"count_converse":count_converse, "liked_converse":liked_converse,"liked_converse_count":liked_converse_count,"disliked_converse":disliked_converse, "disliked_converse_count":disliked_converse_count   }



@app.get("/usertocsv",  status_code=status.HTTP_200_OK)
def user_tocsv(db: Session = Depends(get_db)):
    users = db.query(User).all()

    # Generate the CSV file
    with NamedTemporaryFile(delete=False, mode="w", suffix=".csv",  encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Email","status" , "Registered At"])  # Add column headers
        a = 0
        for user in users:
            csv_writer.writerow([user.name, user.email, user.is_active, user.created_at])  # Replace "other_field" with the actual field name

    response = FileResponse(csvfile.name, media_type="text/csv")
    response.headers["Content-Disposition"] = 'attachment; filename="user_stats.csv"'
    return response

@app.get("/conversestocsv",  status_code=status.HTTP_200_OK)
def converse_tocsv(db: Session = Depends(get_db)):
    converses = db.query(Converse).all()

    # Generate the CSV file
    with NamedTemporaryFile(delete=False, mode="w", suffix=".csv",  encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Query","bot Answer" , "status", "reason", "Registered At"])  # Add column headers
        a = 0
        for converse in converses:
            csv_writer.writerow( [converse.user_name,converse.query,converse.answer,converse.isliked,converse.raison,converse.created_at])  # Replace "other_field" with the actual field name

    response = FileResponse(csvfile.name, media_type="text/csv")
    response.headers["Content-Disposition"] = 'attachment; filename="converse_stats.csv"'
    return response


@app.get("/countlikes", status_code=status.HTTP_200_OK)
def list_message1(db: Session = Depends(get_db)):
    # query = db.query(Converse).group_by(Converse.isliked).all()
    likes = db.query(Converse).filter_by(isliked = False).all()
    likes_count = db.query(Converse).filter_by(isliked = False).count()
    dislikes = db.query(Converse).filter_by(isliked = True).all()
    dislikes_count = db.query(Converse).filter_by(isliked = True).count()
    simples = db.query(Converse).count()
    return {"likes": likes,"likes_count": likes_count, "dislikes": dislikes,"dislikes_count": dislikes_count, "simples": simples  }




@app.get("/countlikes", status_code=status.HTTP_200_OK)
def list_message1(db: Session = Depends(get_db)):
    # query = db.query(Converse).group_by(Converse.isliked).all()
    likes = db.query(Converse).filter_by(isliked = False).all()
    dislikes = db.query(Converse).filter_by(isliked = True).all()
    simples = db.query(Converse).count()
    return {"likes": likes, "dislikes": dislikes, "simples": simples  }




@app.get("/user_count_by_day", status_code=status.HTTP_200_OK)
def get_user_count_by_day(db: Session = Depends(get_db)):

    query = db.query(User.created_at).group_by(User.created_at.date())
    user_count_by_day = query.count().all()

    # Convert the SQLAlchemy results to a list of dictionaries.
    user_count_by_day_list = []
    for created_at, count in user_count_by_day:
        user_count_by_day_list.append({
            "created_at": created_at.date(),
            "count": count
        })

    return user_count_by_day_list


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