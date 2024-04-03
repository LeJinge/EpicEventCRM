from models.models import User
from typing import List
from rich.console import Console


def display_users(users: List[User]):
    console = Console()
    console.print("[bold magenta]Résultats de la recherche[/bold magenta]")
    for index, user in enumerate(users, start=1):
        console.print(f"[bold cyan]{index}.[/bold cyan] {user.first_name} {user.last_name} - {user.role.name}")
