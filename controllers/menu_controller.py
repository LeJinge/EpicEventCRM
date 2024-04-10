import typer

from controllers.client_management import handle_client_management_menu
from controllers.contract_management import handle_contract_management_menu
from controllers.event_management import handle_event_management_menu
from controllers.user_management import handle_collaborator_management_menu
from views.menus import (
    display_management_main_menu,
    display_commercial_main_menu,
    display_support_main_menu
)

app = typer.Typer()


def main_menu(user_role: str):
    while True:
        typer.clear()
        if user_role == "Gestion":
            if not handle_management_main_menu():
                break
        elif user_role == "Commerciale":
            if not handle_commercial_main_menu():
                break
        elif user_role == "Support":
            if not handle_support_main_menu():
                break
        else:
            typer.echo("Rôle non reconnu.")
            break


def handle_management_main_menu():
    while True:
        display_management_main_menu()
        choice = typer.prompt("Entrez votre choix (1-4) ou 0 pour se déconnecter: ", type=int)

        if choice == 1:
            handle_collaborator_management_menu()
        elif choice == 2:
            handle_client_management_menu()
        elif choice == 3:
            handle_contract_management_menu()
        elif choice == 4:
            handle_event_management_menu()
        elif choice == 0:
            return False
        else:
            typer.echo("Choix invalide.")


def handle_commercial_main_menu():
    while True:
        display_commercial_main_menu()
        choice = typer.prompt("Entrez votre choix (1-3) ou 0 pour revenir au menu principal: ", type=int)

        if choice == 1:
            handle_client_management_menu()
        elif choice == 2:
            handle_contract_management_menu()
        elif choice == 3:
            handle_event_management_menu()
        elif choice == 0:
            return False
        else:
            typer.echo("Choix invalide.")


def handle_support_main_menu():
    while True:
        display_support_main_menu()
        choice = typer.prompt("Entrez votre choix (1) ou 0 pour revenir au menu principal: ", type=int)

        if choice == 1:
            handle_event_management_menu()
        elif choice == 0:
            return False
        else:
            typer.echo("Choix invalide.")
