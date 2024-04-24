import typer

from controllers.auth_controller import authenticate_user
from controllers.menu_controller import main_menu
from views.login import get_user_credentials, display_error, display_success

app = typer.Typer()


@app.command()
def login():
    email, password = get_user_credentials()
    connected_user = authenticate_user(email, password)

    if connected_user:
        display_success("Connexion réussie.")
        main_menu(connected_user)
    else:
        display_error("Échec de la connexion. Veuillez vérifier vos identifiants.")
