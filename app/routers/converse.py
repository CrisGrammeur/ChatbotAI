from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
# from 
from models import User, Converse
# from schemas import addConverse
from schemas.converse import addConverse, setLike
# from schemas import addConverse
from crud import get_discussions, get_current_user, create_discussion
# from uuid import uuid4
import uuid

app = APIRouter(
    tags=["converse"],
    prefix="/converse"
)

# @app.get("/", status_code=status.HTTP_200_OK)
# def list_discussion(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     disc = get_discussions(db, current_user.id)
#     return disc

@app.post("/create", status_code=status.HTTP_201_CREATED)
def add_discussion(converse: addConverse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    new_id = str(uuid.uuid4())
    existing_converse = db.query(Converse).filter_by(id=new_id).first()
    while existing_converse:
        # If it exists, generate a new 'id' value
        new_id = str(uuid.uuid4())
        existing_converse = db.query(Converse).filter_by(id=new_id).first()
    data = Converse(
        id = new_id,	
    query = converse.query,
    answer = converse.answer,
    user_id = current_user.id,
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
    converse = db.query(Converse).filter(Converse.id == request_data.converse_id, Converse.user_id == current_user.id).first()
    if not converse:
        raise HTTPException(status_code=404, detail="Converse not found")
    converse.isliked = request_data.is_liked
    db.commit()
    return {"message": "Like status set successfully"}