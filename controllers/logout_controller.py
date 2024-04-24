import typer

from utils.db import SessionLocal
from views.messages import successful_logout


def logout():
    # Créez une instance de session
    db_session = SessionLocal()

    # Fermez la session pour nettoyer les ressources de la base de données
    db_session.close()

    successful_logout()