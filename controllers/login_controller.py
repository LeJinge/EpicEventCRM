import typer

from controllers.auth_controller import authenticate_user
from controllers.menu_controller import main_menu
from utils.db import SessionLocal
from views.login import get_user_credentials, display_error, display_success


def login():
    email, password = get_user_credentials()
    user = authenticate_user(email, password)  # Utiliser directement le résultat de authenticate_user

    if user:
        display_success("Connexion réussie.")
        main_menu(user)  # Passez l'objet user complet
    else:
        display_error("Échec de la connexion. Veuillez vérifier vos identifiants.")

