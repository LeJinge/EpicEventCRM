from controllers.menu_controller import main_menu
from views.connection import get_user_credentials, display_error, display_success
from controllers.auth_controller import authenticate_user
import typer

app = typer.Typer()


@app.command()
def login():
    email, password = get_user_credentials()
    user_role = authenticate_user(email, password)

    if user_role:
        display_success("Connexion réussie.")
        # Appel du menu principal avec le rôle de l'utilisateur
        main_menu(user_role)
    else:
        display_error("Échec de la connexion. Veuillez vérifier vos identifiants.")
