from schemas import UserRequest, UserResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from crud import get_user, get_user_by_email, get_users, create_user, get_current_user
from models import User

app = APIRouter(
    tags=["Users"],
    prefix="/user"
)

# Endpoint pour récupérer la liste des utilisateurs
@app.get("/", status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip,limit)
    return users

# Endpoint pour créer un nouvel utilisateur
@app.post("/register", status_code=status.HTTP_201_CREATED)
def add_user(user: UserRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

# Endpoint pour récupérer un utilisateur par son ID
@app.get("/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @app.put("/modify_login")
# def modify_password(nom: str, email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     user = (db, current_user.id, nom, email)
#     if user is None:
#         raise HTTPException(status_code = 404, detail = "Non retrouvé")
#     return user