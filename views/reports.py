from typing import List

import typer
from rich.console import Console
from rich.table import Table

from models.models import User


def display_users(users: List[User]):
    console = Console()
    console.print("[bold magenta]Résultats de la recherche[/bold magenta]")
    for index, user in enumerate(users, start=1):
        console.print(f"[bold cyan]{index}.[/bold cyan] {user.first_name} {user.last_name} - {user.role.name}")


def display_user_profile(user: User):
    console = Console()
    table = Table(show_header=False, header_style="bold magenta")
    table.add_column("Champ", style="dim", width=12)
    table.add_column("Valeur", justify="right")

    # Ajout des informations de l'utilisateur dans le tableau
    table.add_row("Nom", user.last_name)
    table.add_row("Prénom", user.first_name)
    table.add_row("Email", user.email)
    table.add_row("Rôle", user.role.name)

    # Affichage du tableau
    console.print(table)
