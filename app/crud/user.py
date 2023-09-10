from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from schemas import TokenData
from config.database import get_db
from config.settings import settings
from config.hashing import Hasher

from models import User
from schemas import UserRequest

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scheme_name="JWT")

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserRequest):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = User(
        name = user.name,
        email = user.email,
        hashed_password = hashed_password,
        bio = user.bio,
        location = user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db, email)
    # print(user)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Mail incorect",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    if not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Mot de passe incorect",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
        mail: str = payload.get("sub")
        print("mail extracted is ",mail)
        if mail is None:
            raise credentials_exception
        token_data = TokenData(mail = mail)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.mail)
    if user is None:
        raise credentials_exception
    return user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
