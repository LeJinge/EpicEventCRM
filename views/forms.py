import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from models.models import UserRole, Client, User
from utils.db import SessionLocal


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

    db: Session = SessionLocal()
    commerciaux = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
    db.close()

    typer.echo("Commerciaux disponibles :")
    for index, commercial in enumerate(commerciaux, start=1):
        typer.echo(f"{index}. {commercial.first_name} {commercial.last_name}")

    commercial_index = typer.prompt("Sélectionnez le numéro du commercial assigné (laissez vide si aucun)", default="",
                                    show_default=False)
    commercial_id = commerciaux[int(commercial_index) - 1].id if commercial_index.isdigit() and 0 < int(
        commercial_index) <= len(commerciaux) else None

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,
        "commercial_id": commercial_id  # Ajoutez cet identifiant à votre dictionnaire de retour
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
    # Dans le formulaire de mise à jour client
    commercial_index = typer.prompt("Sélectionnez le numéro du commercial assigné (laissez vide si aucun)", default="",
                                    show_default=False)

    # Assurez-vous que commercial_index est un entier et dans la plage valide, sinon commercial_id est None
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
