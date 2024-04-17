from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from models.models import UserRole, Client, User, ContractStatus, Contract, Event
from utils.choose_items import choose_client, choose_commercial, choose_contract, choose_support_contact
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.reports import display_users


def user_form() -> dict:
    """Collecte les informations pour la création d'un collaborateur."""
    first_name = typer.prompt("Prénom du collaborateur")
    last_name = typer.prompt("Nom du collaborateur")
    email = typer.prompt("Email du collaborateur")
    role_str = typer.prompt("Rôle du collaborateur (ex: Gestion, Commerciale, Support)")
    password = typer.prompt("Mot de passe du collaborateur", confirmation_prompt=True, hide_input=True)

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "role_str": role_str,
        "password": password
    }


def user_update_form(user):
    first_name = typer.prompt(f"Prénom ({user.first_name})", default=user.first_name, show_default=False)
    last_name = typer.prompt(f"Nom ({user.last_name})", default=user.last_name, show_default=False)
    email = typer.prompt(f"Email ({user.email})", default=user.email, show_default=False)

    # Afficher les rôles disponibles
    roles = [role.value for role in UserRole]  # Assurez-vous que UserRole est votre Enum de rôles
    typer.echo("Rôles disponibles : " + ", ".join(roles))
    role_str = typer.prompt(f"Rôle ({user.role.value})", default=user.role.value, show_default=False)

    # Retourner un dictionnaire des valeurs mises à jour
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'role_str': role_str
    }


def client_form() -> dict:
    """Collecte les informations pour la création d'un client."""
    first_name = typer.prompt("Prénom du client")
    last_name = typer.prompt("Nom du client")
    email = typer.prompt("Email du client")
    phone_number = typer.prompt("Numéro de téléphone du client")
    company_name = typer.prompt("Nom de l'entreprise du client")
    commercial_id = choose_commercial()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_id": commercial_id
    }


def client_update_form(client: Client) -> dict:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Numéro", style="dim", width=12)
    table.add_column("Prénom", min_width=20)
    table.add_column("Nom", min_width=20)

    # Récupération des commerciaux
    db: Session = SessionLocal()
    commerciaux = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
    db.close()

    # Affichage des commerciaux disponibles
    console.print("\nCommerciaux disponibles :")
    for index, commercial in enumerate(commerciaux, start=1):
        table.add_row(str(index), commercial.first_name, commercial.last_name)
    console.print(table)

    # Sélection du commercial
    commercial_index = typer.prompt("Sélectionnez le numéro du commercial assigné (laissez vide si aucun)", default="",
                                    show_default=False)

    if commercial_index.isdigit() and 0 < int(commercial_index) <= len(commerciaux):
        commercial_id = commerciaux[int(commercial_index) - 1].id
    else:
        commercial_id = None

    # Mise à jour des autres informations du client
    first_name = typer.prompt("Prénom", default=client.first_name, show_default=True)
    last_name = typer.prompt("Nom", default=client.last_name, show_default=True)
    email = typer.prompt("Email", default=client.email, show_default=True)
    phone_number = typer.prompt("Numéro de téléphone", default=client.phone_number, show_default=True)
    company_name = typer.prompt("Nom de l'entreprise", default=client.company_name, show_default=True)

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_id": commercial_id
    }


def contract_form():
    client_id = choose_client()
    if client_id is None:
        return None

    commercial_contact_id = choose_commercial()
    if commercial_contact_id is None:
        return None

    typer.echo("Choisissez le statut du contrat :")
    typer.echo("1. In Progress")
    typer.echo("2. Signed")
    typer.echo("3. Finished")
    status_choice = typer.prompt("Entrez le numéro correspondant au statut", type=int)

    status_map = {1: "IN_PROGRESS", 2: "SIGNED", 3: "FINISHED"}
    status_key = status_map.get(status_choice)
    if status_key is None or status_key not in ContractStatus._value2member_map_:
        typer.echo("Choix de statut invalide.")
        return None
    status = status_key

    total_amount = int(typer.prompt("Montant total du contrat"))
    remaining_amount = int(typer.prompt("Montant restant du contrat"))
    creation_date = datetime.today().strftime("%Y-%m-%d")

    return {
        "client_id": client_id,
        "commercial_contact_id": commercial_contact_id,
        "status": status,  # Utilisation directe de la valeur de l'énumération
        "total_amount": total_amount,
        "remaining_amount": remaining_amount,
        "creation_date": creation_date,
    }


def contract_update_form(contract):
    typer.echo(f"Mise à jour du contrat ID: {contract.id}")

    # Mise à jour du statut
    typer.echo("Choisissez le statut du contrat :")
    status_options = list(ContractStatus)
    for idx, status in enumerate(status_options, start=1):
        typer.echo(f"{idx}. {status.value}")

    status_choice = typer.prompt("Entrez le numéro correspondant au statut (laissez vide pour ne pas modifier) :",
                                 default="", show_default=False)
    if status_choice.isdigit() and 0 < int(status_choice) <= len(status_options):
        status = status_options[int(status_choice) - 1].value
    else:
        status = contract.status  # Conserve la valeur actuelle si aucune nouvelle entrée

    # Montants (inchangés)
    total_amount = int(typer.prompt("Montant total du contrat (laisser vide pour ne pas modifier): ",
                                    default=str(contract.total_amount)))
    remaining_amount = int(typer.prompt("Montant restant du contrat (laisser vide pour ne pas modifier): ",
                                        default=str(contract.remaining_amount)))

    # Sélection du contact commercial
    typer.echo("Sélectionnez un nouveau contact commercial (laissez vide pour ne pas changer) :")
    with SessionLocal() as db:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        if commercials:
            selected_commercial_id = paginate_items(commercials, display_users,
                                                      10)  # Utilisation de paginate_items pour l'affichage
            if selected_commercial_id is None:
                selected_commercial_id = contract.commercial_contact_id  # Conserver l'ID existant si aucune entrée
        else:
            selected_commercial_id = contract.commercial_contact_id  # Aucun commercial disponible

    return {
        "status": status,
        "total_amount": total_amount,
        "remaining_amount": remaining_amount,
        "commercial_contact_id": selected_commercial_id
    }


def event_form():
    db: Session = SessionLocal()
    try:
        title = typer.prompt("Titre de l'événement")
        start_date = typer.prompt("Date de début de l'événement (format YYYY-MM-DD)", type=str)
        end_date = typer.prompt("Date de fin de l'événement (format YYYY-MM-DD)", type=str)
        location = typer.prompt("Lieu de l'événement")
        attendees = int(typer.prompt("Nombre de participants"))
        notes = typer.prompt("Notes supplémentaires", default="")

        typer.echo("Sélectionnez un client pour l'événement :")
        client_id = choose_client()
        if client_id is None:
            return None

        typer.echo("Sélectionnez un contrat pour l'événement :")
        contract_id = choose_contract()
        if contract_id is None:
            return None

        typer.echo("Voulez-vous sélectionner un contact de support maintenant ? (Oui/Non)")
        add_support_now = typer.prompt("Votre choix")
        if add_support_now.lower() == 'oui':
            typer.echo("Sélectionnez un contact de support pour l'événement :")
            support_contact_id = choose_support_contact()
            if support_contact_id is None:
                return None
        else:
            support_contact_id = None  # L'utilisateur a choisi de ne pas ajouter de contact de support maintenant

        return {
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "attendees": attendees,
            "notes": notes,
            "client_id": client_id,
            "contract_id": contract_id,
            "support_contact_id": support_contact_id
        }
    finally:
        db.close()


def event_update_form(event):
    db: Session = SessionLocal()
    try:
        title = typer.prompt("Titre de l'événement", default=event.title)
        start_date = typer.prompt("Date de début de l'événement (format YYYY-MM-DD)", default=event.start_date.strftime("%Y-%m-%d"))
        end_date = typer.prompt("Date de fin de l'événement (format YYYY-MM-DD)", default=event.end_date.strftime("%Y-%m-%d"))
        location = typer.prompt("Lieu de l'événement", default=event.location)
        attendees = int(typer.prompt("Nombre de participants", default=str(event.attendees)))
        notes = typer.prompt("Notes supplémentaires", default=event.notes)

        typer.echo("Modifier le client pour l'événement ? (Oui pour changer, appuyez sur Entrée pour garder l'actuel)")
        if typer.confirm('text'):
            client_id = choose_client()
        else:
            client_id = event.client_id

        typer.echo("Modifier le contrat pour l'événement ? (Oui pour changer, appuyez sur Entrée pour garder l'actuel)")
        if typer.confirm('text'):
            contract_id = choose_contract()
        else:
            contract_id = event.contract_id

        typer.echo("Modifier le contact de support pour l'événement ? (Oui pour changer, appuyez sur Entrée pour garder l'actuel)")
        if typer.confirm('text'):
            support_contact_id = choose_support_contact()
        else:
            support_contact_id = event.support_contact_id

        return {
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "attendees": attendees,
            "notes": notes,
            "client_id": client_id,
            "contract_id": contract_id,
            "support_contact_id": support_contact_id
        }
    finally:
        db.close()
