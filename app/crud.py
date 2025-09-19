from sqlalchemy.orm import Session
from .models import User

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_uuid: str):
    return db.query(User).filter(User.uuid == user_uuid).first()

def create_user(db: Session, user_data):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_uuid: str, user_data):
    user = get_user(db, user_uuid)
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_uuid: str):
    user = get_user(db, user_uuid)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user