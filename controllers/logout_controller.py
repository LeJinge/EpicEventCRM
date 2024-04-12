import typer

from utils.db import SessionLocal


def logout():
    # Créez une instance de session
    db_session = SessionLocal()

    # Fermez la session pour nettoyer les ressources de la base de données
    db_session.close()

    typer.echo("Déconnexion réussie.")