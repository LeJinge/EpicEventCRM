import sentry_sdk
import typer

from config import load_config
from controllers.login_controller import login

# Load config.yaml
config = load_config('config.yaml')

sentry_api_key = config["sentry"].get("SENTRY_API_KEY")


# Initialisation de Sentry
sentry_sdk.init(
    dsn=sentry_api_key,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = typer.Typer()


# Ajoutez ici d'autres commandes si nécessaire

@app.command()
def run():
    login()


if __name__ == "__main__":
    app()
