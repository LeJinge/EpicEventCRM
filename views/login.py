from rich.console import Console
from getpass import getpass
from utils.validation import is_valid_email

console = Console()


def get_user_credentials():
    email = console.input("[bold magenta]Email: [/bold magenta]")
    while not is_valid_email(email):
        console.print("[bold red]Email invalide. Veuillez réessayer.[/bold red]", style="bold red")
        email = console.input("[bold magenta]Email: [/bold magenta]")
    password = getpass("Mot de passe: ")
    return email, password


def display_error(message):
    console.print(f"[bold red]Erreur[/bold red]: {message}")


def display_success(message):
    console.print(f"[bold green]Succès[/bold green]: {message}", style="bold green")
