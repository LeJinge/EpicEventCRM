import typer

from controllers.login_controller import login

app = typer.Typer()

# Ajoutez ici d'autres commandes si nécessaire

app.command()(login)  # Associe la commande de connexion Typer à la fonction login_controller

if __name__ == "__main__":
    app()
