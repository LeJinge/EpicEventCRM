from typing import List

from rich.console import Console
from rich.table import Table

from models.models import User, Client, Contract, Event


def display_users(users: List[User], start_index: int) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Numéro", style="dim", width=6)
    table.add_column("ID", width=12)
    table.add_column("Nom", min_width=20)
    table.add_column("Email", min_width=20)
    table.add_column("Rôle", min_width=20)

    for index, user in enumerate(users, start=start_index):
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

        role_str = str(user.role) if user.role is not None else "N/A"

        table.add_row(
            str(index),
            str(user.id),
            full_name,
            user.email or "",
            role_str
        )

    return table


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


# Vue pour afficher les controllers de gestion des clients


def display_clients(clients: List[Client], start_index: int) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Numéro", style="dim", width=6)  # Unifié avec "Numéro" comme dans display_users
    table.add_column("ID", width=12)
    table.add_column("Prénom et Nom", min_width=40)  # Combiné pour la cohérence
    table.add_column("Nom de l'entreprise", min_width=20)
    table.add_column("Email", min_width=20)
    table.add_column("Contact Commercial", min_width=30)  # Plus large pour noms complets

    for index, client in enumerate(clients, start=start_index):
        full_name = f"{client.first_name or ''} {client.last_name or ''}".strip()
        company_name = client.company_name or "N/A"
        email = client.email or "N/A"
        commercial_full_name = "N/A"

        if client.commercial_contact:
            commercial_full_name = f"{client.commercial_contact.first_name or ''} {client.commercial_contact.last_name or ''}".strip()

        table.add_row(
            str(index),
            str(client.id),
            full_name,
            company_name,
            email,
            commercial_full_name
        )

    return table


def display_client_profile(client: Client):
    console = Console()
    table = Table(show_header=False, header_style="bold magenta")
    table.add_column("Champ", style="dim", width=12)
    table.add_column("Valeur", justify="right")

    # Ajout des informations du client dans le tableau
    table.add_row("Nom", client.last_name or "N/A")
    table.add_row("Prénom", client.first_name or "N/A")
    table.add_row("Email", client.email or "N/A")
    table.add_row("Numéro de téléphone", client.phone_number or "N/A")
    table.add_row("Nom de l'entreprise", client.company_name or "N/A")

    commercial_full_name = "N/A"
    if client.commercial_contact:
        commercial_full_name = f"{client.commercial_contact.first_name or ''} {client.commercial_contact.last_name or ''}".strip()
    table.add_row("Commerciale", commercial_full_name)

    # Affichage du tableau
    console.print(table)


# Vue pour afficher les controllers de gestion des contrats

def display_contracts(contracts: List[Contract], start_index: int) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Index", style="dim", width=6)
    table.add_column("ID", width=12)
    table.add_column("Client", min_width=20)
    table.add_column("Contact Commercial", min_width=20)
    table.add_column("Statut", min_width=20)
    table.add_column("Montant Total", min_width=20)
    table.add_column("Montant Restant", min_width=20)
    table.add_column("Date de Création", min_width=20)

    for index, contract in enumerate(contracts, start=start_index):
        client_name = f"{contract.client.first_name} {contract.client.last_name}"
        commercial_name = f"{contract.commercial_contact.first_name} {contract.commercial_contact.last_name}"
        status = contract.status.name  # Assumant que 'status' est un Enum
        creation_date = contract.creation_date.strftime("%Y-%m-%d")

        table.add_row(
            str(index),
            str(contract.id),
            client_name,
            commercial_name,
            status,
            str(contract.total_amount),
            str(contract.remaining_amount),
            creation_date
        )

    return table


def display_contract_profile(contract: Contract):
    console = Console()
    table = Table(show_header=False, header_style="bold magenta")
    table.add_column("Champ", style="dim", width=20)
    table.add_column("Valeur", min_width=20)

    client_name = f"{contract.client.first_name} {contract.client.last_name}"
    commercial_name = f"{contract.commercial_contact.first_name} {contract.commercial_contact.last_name}"
    status = contract.status.name  # Assumant que 'status' est un Enum
    creation_date = contract.creation_date.strftime("%Y-%m-%d")

    table.add_row("Client", client_name)
    table.add_row("Contact Commercial", commercial_name)
    table.add_row("Statut", status)
    table.add_row("Montant Total", str(contract.total_amount))
    table.add_row("Montant Restant", str(contract.remaining_amount))
    table.add_row("Date de Création", creation_date)

    console.print(table)


def display_events(events: List[Event], start_index: int) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Index", style="dim", width=6)
    table.add_column("ID", width=12)
    table.add_column("Nom", min_width=20)
    table.add_column("Date de Début", min_width=20)
    table.add_column("Date de Fin", min_width=20)
    table.add_column("Lieu", min_width=20)
    table.add_column("Client", min_width=20)
    table.add_column("Contact Support", min_width=20)
    table.add_column("Nombre de Participants", min_width=20)
    table.add_column("Identifiant du Contrat", min_width=20)

    for index, event in enumerate(events, start=start_index):
        client_name = f"{event.client.first_name} {event.client.last_name}"
        support_name = event.support_contact.first_name + " " + event.support_contact.last_name if event.support_contact else "Non assigné"
        start_date = event.start_date.strftime("%Y-%m-%d")
        end_date = event.end_date.strftime("%Y-%m-%d")

        table.add_row(
            str(index),
            str(event.id),
            event.title,
            start_date,
            end_date,
            event.location,
            client_name,
            support_name,
            str(event.attendees),
            str(event.contract_id)
        )

    return table


def display_event_profile(event: Event):
    console = Console()
    table = Table(show_header=False, header_style="bold magenta")
    table.add_column("Champ", style="dim", width=20)
    table.add_column("Valeur", min_width=20)

    client_name = f"{event.client.first_name} {event.client.last_name}"
    if event.support_contact:
        support_name = f"{event.support_contact.first_name} {event.support_contact.last_name}"
    else:
        support_name = "Non assigné"
    start_date = event.start_date.strftime("%Y-%m-%d")
    end_date = event.end_date.strftime("%Y-%m-%d")
    location = event.location
    attendees = event.attendees

    table.add_row("Client", client_name)
    table.add_row("Contact Support", support_name)
    table.add_row("Date de Début", start_date)
    table.add_row("Date de Fin", end_date)
    table.add_row("Lieu", location)
    table.add_row("Nombre de Participants", str(attendees))

    console.print(table)
