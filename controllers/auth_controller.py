from models.models import User
from utils.db import SessionLocal  # Assurez-vous que cette fonction est correctement définie
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(email: str, password: str) -> str:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user and user.verify_password(password):
            return user.role.value  # Retourner le rôle de l'utilisateur
    finally:
        session.close()
    return None  # Retourner None si l'authentification échoue
