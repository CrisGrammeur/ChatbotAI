from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from sqlalchemy import func
# from 
from models import User, Converse, User_chat, eventConverse, User_Eventchat
# from schemas import addConverse
from schemas.converse import addConverse, setLike,settrash
# from schemas import addConverse
from crud import get_discussions, get_current_user, create_discussion
# from uuid import uuid4
import uuid
from datetime import datetime

app = APIRouter(
    tags=["eventconverse"],
    prefix="/eventconverse"
)

# @app.get("/", status_code=status.HTTP_200_OK)
# def list_discussion(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     disc = get_discussions(db, current_user.id)
#     return disc

@app.get("/", status_code=status.HTTP_200_OK)
def list_discussion(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # converses = db.query(Converse).all()
    converses = db.query(eventConverse).filter(eventConverse.user_id== current_user.id).all()
    converse_grouped_by_user_chat_id = {}
    for converse in converses:
        user_chat_id = converse.user_chat_id
        if user_chat_id not in converse_grouped_by_user_chat_id:
            converse_grouped_by_user_chat_id[user_chat_id] = []
        converse_grouped_by_user_chat_id[user_chat_id].append(converse)
    return list(converse_grouped_by_user_chat_id.values())

@app.get("/{id}", status_code=status.HTTP_200_OK)
def get_discussion(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    disc = db.query(eventConverse).filter_by(id=id).first()
    return disc

@app.post("/", status_code=status.HTTP_201_CREATED)
def add_discussion(converse: addConverse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_id = str(uuid.uuid4())


@app.post("/create", status_code=status.HTTP_201_CREATED)
def add_discussion(converse: addConverse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    new_id = str(uuid.uuid4())
    existing_converse = db.query(eventConverse).filter_by(id=new_id).first()
    while existing_converse:
        # If it exists, generate a new 'id' value
        new_id = str(uuid.uuid4())
        existing_converse = db.query(eventConverse).filter_by(id=new_id).first()
    if converse.chat_id == "null":
        chat_id = str(uuid.uuid4())
        existing_chat = db.query(eventConverse).filter_by(user_chat_id=chat_id).first()
        while existing_chat:
            chat_id = str(uuid.uuid4())
        existing_chat = db.query(eventConverse).filter_by(user_chat_id=chat_id).first()
        chat = User_chat(
                key = chat_id,
                date = datetime.now(),
                user_id = current_user.id,)
        db.add(chat)
        db.commit()
        db.refresh(chat)
    else:
        chat_id = converse.chat_id
        
    data = eventConverse(
    id = new_id,
    user_chat_id = chat_id,	
    query = converse.query,
    answer = converse.answer,
    user_id = current_user.id,
    user_name = current_user.name,
    )
    print(converse)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
    # disc = create_discussion(db, current_user.id, chat)
    # return disc
    

@app.put("/set_like")
async def set_like( request_data: setLike, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # converse = db.query(Converse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    converse = db.query(eventConverse).filter(eventConverse.id == request_data.converse_id, eventConverse.user_id == current_user.id).first()
    
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.isliked = request_data.is_liked
    converse.raison = request_data.reason
    converse.user_name = current_user.name
    db.commit()
    return {"message": "Like status set successfully"}

@app.put("/trash")
async def trash( request_data: settrash, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    converse = db.query(eventConverse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    # converse = db.query(Converse).filter(Converse.id == current_user.id, Converse.user_id == current_user.id).first()
    # converse = db.query(Converse).filter(and_(Converse.user_id == current_user.id, Converse.id == request_data.converse_id)).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.is_deleted = True
    db.commit()
    return {"message": "Converse trashed successfully"}

@app.put("/delete")
async def delete( request_data: settrash, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    converse = db.query(eventConverse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    db.delete(converse)
    db.commit()
    return {"message": "Converse deleted successfully"}

@app.put("/untrash")
async def untrash( request_data: settrash, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    converse = db.query(eventConverse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.is_deleted = False
    db.commit()
    return {"message": "Converse untrashed successfully"}

@app.put("/restore")
async def restore( request_data: settrash, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    converse = db.query(eventConverse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.is_deleted = False
    converse.is_trashed = False
    db.commit()
    return {"message": "Converse restored successfully"}
@app.delete("/delete")
async def delete( request_data: settrash, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    converse = db.query(eventConverse).filter(id = request_data.converse_id, user_id = current_user.id).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.is_deleted = True
    db.commit()
    return {"message": "Converse deleted successfully"}
