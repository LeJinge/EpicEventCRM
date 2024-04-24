from rich.console import Console
from rich.table import Table

from models.models import User
from utils.permissions import is_superuser, is_gestion, is_commerciale, is_support

console = Console()


def display_menu(title: str, options: list[str]) -> None:
    """
    Affiche un menu avec des options dans un format enrichi.
    """
    table = Table(title=title, show_header=False, title_style="bold magenta")

    for option in options:
        table.add_row(option)

    console.print(table)


def display_main_menu(connected_user: User) -> None:
    title = "Menu Principal"

    # D'abord, déterminez le rôle de l'utilisateur
    if is_superuser(connected_user):
        options = [
            "1. Recherche",
            "2. Gestion des collaborateurs",
            "3. Gestion des clients",
            "4. Gestion des contrats",
            "5. Gestion des évènements",
            "0. Quitter",
        ]
    elif is_gestion(connected_user):
        options = [
            "1. Recherche",
            "2. Gestion des collaborateurs",
            "3. Gestion des contrats",
            "4. Gestion des évènements",
            "0. Quitter",
        ]
    elif is_commerciale(connected_user):
        options = [
            "1. Recherche",
            "2. Gestion des clients",
            "3. Gestion des contrats",
            "4. Gestion des évènements",
            "0. Quitter",
        ]
    elif is_support(connected_user):
        options = [
            "1. Recherche",
            "2. Gestion des évènements",
            "0. Quitter",
        ]
    else:
        options = []

    # Affichez le menu avec les options appropriées
    display_menu(title, options)


def display_search_menu() -> None:
    title = "Menu de Recherche"
    options = [
        "1. Rechercher des collaborateurs",
        "2. Rechercher des clients",
        "3. Rechercher des contrats",
        "4. Rechercher des évènements",
    ]
    display_menu(title, options)


# Affichage des menus de gestion des collaborateurs
def display_user_management_menu(connected_user: User) -> None:
    title = "Gestion des Collaborateurs"
    if is_superuser(connected_user) or is_gestion(connected_user):
        options = [
            "1. Créer un collaborateur",
            "2. Rechercher un collaborateur",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_search_user_menu(connected_user: User):
    title = "Recherche de Collaborateurs"
    if is_superuser(connected_user) or is_gestion(connected_user):
        options = [
            "1. Rechercher par nom",
            "2. Rechercher par équipe",
            "3. Tous les collaborateurs",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_user_options(connected_user: User):
    title = "Options disponibles pour collaborateur"
    if is_superuser(connected_user):
        options = [
            "1. Modifier ce collaborateur",
            "2. Supprimer ce collaborateur",
            "0. Retour",
        ]
    elif is_gestion(connected_user):
        options = [
            "1. Modifier ce collaborateur",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


# Affichage des menus de gestion des clients
def display_client_management_menu(connected_user: User) -> None:
    title = "Gestion des Clients"
    if is_superuser(connected_user) or is_commerciale(connected_user):
        options = [
            "1. Créer un client",
            "2. Rechercher un client",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_search_client_menu(connected_user: User):
    title = "Recherche de Clients"
    if is_superuser(connected_user) or is_commerciale(connected_user):
        options = [
            "1. Rechercher par nom",
            "2. Rechercher par commercial",
            "3. Tous les clients",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_client_options(connected_user: User):
    title = "Options disponibles pour ce client"
    if is_superuser(connected_user):
        options = [
            "1. Modifier ce client",
            "2. Supprimer ce client",
            "0. Retour",
        ]
    elif is_commerciale(connected_user):
        options = [
            "1. Modifier ce client",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


# Affichage des menus de gestion des contrats
def display_contract_management_menu(connected_user: User) -> None:
    title = "Gestion des Contrats"
    if is_superuser(connected_user) or is_gestion(connected_user):
        options = [
            "1. Créer un contrat",
            "2. Rechercher un contrat",
            "0. Retour",
        ]
    elif is_commerciale(connected_user):
        options = [
            "1. Rechercher un contrat",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_search_contract_menu(connected_user: User):
    title = "Recherche de Contrats"
    if is_superuser(connected_user) or is_commerciale(connected_user) or is_gestion(connected_user):

        options = [
            "1. Rechercher par client",
            "2. Rechercher par commercial",
            "3. Contrats en cours",
            "4. Contrats non entièrement payés",
            "5. Tous les contrats",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_contract_options(connected_user: User):
    title = "Options disponibles pour ce contrat"
    if is_superuser(connected_user):
        options = [
            "1. Modifier ce contrat",
            "2. Supprimer ce contrat",
            "0. Retour",
        ]
    elif is_commerciale(connected_user):
        options = [
            "1. Modifier ce contrat",
            "0. Retour",
        ]
    else:
        options = [
            "0. Retour",
        ]
    display_menu(title, options)


# Affichage des menus de gestion des évènements
def display_event_management_menu(connected_user: User) -> None:
    title = "Gestion des Évènements"
    if is_superuser(connected_user) or is_commerciale(connected_user):
        options = [
            "1. Créer un évènement",
            "2. Rechercher un évènement",
            "0. Retour",
        ]
    elif is_gestion(connected_user) or is_support(connected_user):
        options = [
            "1. Rechercher un évènement",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_search_event_menu(connected_user: User):
    title = "Recherche d'Évènements"
    if is_superuser(connected_user) or is_support(connected_user) or is_gestion(connected_user) or is_commerciale(connected_user):
        options = [
            "1. Rechercher par contrat",
            "2. Rechercher par support",
            "3. Évènements sans support",
            "4. Rechercher par client",
            "5. Tous les évènements",
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)


def display_event_options(connected_user: User):
    title = "Options disponibles pour cet évènement"
    if is_superuser(connected_user):
        options = [
            "1. Modifier cet évènement",
            "2. Supprimer cet évènement",
            "0. Retour",
        ]
    elif is_gestion(connected_user) or is_support(connected_user):
        options = [
            "1. Modifier cet évènement",
            "0. Retour",
        ]
    elif is_commerciale(connected_user):
        options = [
            "0. Retour",
        ]
    else:
        options = ["Accès refusé."]
    display_menu(title, options)
