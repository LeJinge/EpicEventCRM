import typer

from models.models import UserRole


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

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name
    }


def client_update_form(client):
    first_name = typer.prompt(f"Prénom ({client.first_name})", default=client.first_name, show_default=False)
    last_name = typer.prompt(f"Nom ({client.last_name})", default=client.last_name, show_default=False)
    email = typer.prompt(f"Email ({client.email})", default=client.email, show_default=False)
    phone_number = typer.prompt(f"Numéro de téléphone ({client.phone_number})", default=client.phone_number,
                                show_default=False)
    company_name = typer.prompt(f"Nom de l'entreprise ({client.company_name})", default=client.company_name,
                                show_default=False)
    return first_name, last_name, email, phone_number, company_name
