from models.models import User
from utils.db import SessionLocal
from utils.security import pwd_context


def authenticate_user(email: str, password: str) -> User:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user and pwd_context.verify(password, user.password):
            return user  # Retourner l'objet User complet
    finally:
        session.close()
    return None  # Retourner None si l'authentification échoue
