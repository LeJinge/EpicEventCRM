from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from models.models import UserRole, Client, User, ContractStatus, Contract
from utils.choose_items import choose_client, choose_commercial
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
    return first_name, last_name, email, role_str


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


def contract_update_form(contract: Contract):
    typer.echo(f"Mise à jour du contrat ID: {contract.id}")

    typer.echo("Choisissez le statut du contrat :")
    for idx, status in enumerate(ContractStatus, start=1):
        typer.echo(f"{idx}. {status.value}")

    status_choice = typer.prompt("Entrez le numéro correspondant au statut", type=int)
    status_options = list(ContractStatus)
    if status_choice < 1 or status_choice > len(status_options):
        typer.echo("Choix de statut invalide.")
        return None

    status = status_options[status_choice - 1].value

    total_amount = int(typer.prompt("Montant total du contrat (laisser vide pour ne pas modifier): ",
                                    default=str(contract.total_amount)))
    remaining_amount = int(typer.prompt("Montant restant du contrat (laisser vide pour ne pas modifier): ",
                                        default=str(contract.remaining_amount)))

    # Afficher la liste des commerciaux pour la sélection
    typer.echo("Sélectionnez un nouveau contact commercial (laissez vide pour ne pas changer) :")
    with SessionLocal() as db:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        selected_commercial_id = paginate_items(commercials, display_users, 10) if commercials else None

    return {
        "status": status,
        "total_amount": total_amount,
        "remaining_amount": remaining_amount,
        "commercial_contact_id": selected_commercial_id,  # Ajouter l'ID du commercial sélectionné
    }
