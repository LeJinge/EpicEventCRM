from sqlalchemy.orm import Session
from models.models import User
from utils.db import SessionLocal

# Supposons que cette variable globale stocke l'ID de l'utilisateur courant.
# Dans une application réelle, vous voudriez gérer ceci de manière plus sécurisée, peut-être avec des jetons de session.
CURRENT_USER_ID = None


def get_current_user() -> User:
    """
    Récupère l'utilisateur courant à partir de la base de données en utilisant l'ID stocké dans CURRENT_USER_ID.
    Retourne l'instance de l'utilisateur ou None si aucun utilisateur n'est connecté ou si l'utilisateur n'est pas trouvé.
    """
    if CURRENT_USER_ID is None:
        return None

    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == CURRENT_USER_ID).first()
    db.close()
    return user
