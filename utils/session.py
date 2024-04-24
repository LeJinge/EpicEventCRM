from models.models import User
from utils.db import SessionLocal


CURRENT_USER_ID = None


def get_current_user() -> User:
    if CURRENT_USER_ID is None:
        return None

    with SessionLocal() as db:
        user = db.query(User).filter(User.id == CURRENT_USER_ID).first()
    return user

