import sentry_sdk
import typer

from controllers.login_controller import login

# Initialisation de Sentry
sentry_sdk.init(
    dsn="https://0f22d1ce60e139ab2a2dfa3178c7d010@o4507101273718784.ingest.de.sentry.io/4507101277585488",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = typer.Typer()

# Ajoutez ici d'autres commandes si nécessaire

app.command()(login)  # Associe la commande de connexion Typer à la fonction login_controller

if __name__ == "__main__":
    app()
