from sqlalchemy.orm import Session

from models import Discussion, Chat
from schemas import DiscussionRequest

def get_discussions(db: Session, id: str):
    dis = ( db.query(Discussion)
                # .join(Chat)
                .outerjoin(Chat, Discussion.id == Chat.discussion_id)
                .filter(Discussion.user_id == id)
                .all()
    )
    return dis

def get_discussion(db: Session, user_id: str, discussion_id: str):
    dis = db.query(Discussion).filter(Discussion.user_id == user_id, Discussion.id == discussion_id).first()
    return dis

def create_discussion(db: Session, user_id: str, discussion: str):
    db_disc = Discussion(
        user_id=user_id,
        title=discussion
    )
    db.add(db_disc)
    db.commit()
    db.refresh(db_disc)
    return db_disc