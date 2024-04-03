from rich.console import Console
from utils.validation import is_valid_email

console = Console()


def get_user_credentials():
    while True:
        email = input("Email: ")
        if not is_valid_email(email):
            console.print("[bold red]Email invalide. Veuillez réessayer.[/bold red]")
            continue
        break
    password = input(
        "Mot de passe: ")  # Dans une application réelle, envisagez d'utiliser getpass pour masquer l'entrée
    return email, password


def display_error(message):
    console.print(f"[bold red]Erreur[/bold red]: {message}")


def display_success(message):
    console.print(f"[bold green]Succès[/bold green]: {message}", style="bold green")
