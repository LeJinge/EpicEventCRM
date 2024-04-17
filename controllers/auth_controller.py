from models.models import User
from utils.db import SessionLocal
from utils.security import pwd_context


def authenticate_user(email: str, password: str) -> User:
    session = SessionLocal()
    try:
        connected_user = session.query(User).filter(User.email == email).first()
        if connected_user and pwd_context.verify(password, connected_user.password):
            return connected_user
    finally:
        session.close()
    return None
