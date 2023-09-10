from config.settings import settings
from schemas import Token
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from crud import authenticate_user, get_user, get_current_user, create_access_token
from models import User
from datetime import datetime, timedelta


app = APIRouter(
    prefix='/login',
    tags = ['Log']
)

@app.post("/token", response_model = Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Mot de passe ou Mail incorecte"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.email}, expires_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_user_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    me = get_user(db, current_user.id)
    return me

# @router.put("/modify_password")
# def modify_password(mdp: schemas.mdpRequest, db: Session = Depends(get_db), current_user: models.Login = Depends(get_current_user)):
#     user = crud_sys.modify_password(db, current_user.id, mdp)
#     if user is None:
#         raise HTTPException(status_code = 404, detail = "Non retrouvé")
#     return user