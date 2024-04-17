import traceback
import typer
from sqlalchemy.orm import Session, joinedload

from models.models import Client, User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.permissions import is_superuser, is_commerciale
from utils.validation import validate_client_data
from views.forms import client_form, client_update_form
from views.reports import display_client_profile, display_clients, display_users


# Gère l'ajout d'un nouveau client
def add_client(connected_user: User):
    if is_superuser(connected_user) or is_commerciale(connected_user):
        client_data = client_form()
        try:
            # Valider les données du client
            validate_client_data(
                first_name=client_data['first_name'],
                last_name=client_data['last_name'],
                email=client_data['email'],
                phone_number=client_data['phone_number'],
                company_name=client_data['company_name']
            )

            commercial_contact_id = client_data.get('commercial_id')
            if not commercial_contact_id:
                raise ValueError("Un ID commercial doit être fourni.")

            db: Session = SessionLocal()

            # Vérifier si l'ID commercial correspond à un utilisateur avec le rôle COMMERCIALE
            commercial_user = db.query(User).filter(User.id == commercial_contact_id,
                                                    User.role == UserRole.COMMERCIALE).first()
            if not commercial_user:
                raise ValueError("L'ID commercial fourni ne correspond à aucun commercial valide.")

            client = Client(
                first_name=client_data['first_name'],
                last_name=client_data['last_name'],
                email=client_data['email'],
                phone_number=client_data['phone_number'],
                company_name=client_data['company_name'],
                commercial_contact_id=commercial_contact_id
            )
            db.add(client)
            db.commit()
            db.refresh(client)
            db.close()

            typer.echo(f"Client {client.first_name} {client.last_name} créé avec succès.")
            return
        except ValueError as e:
            typer.echo(f"Erreur: {e}")
        except Exception as e:
            typer.echo(f"Une erreur inattendue est survenue : {e}")
    else:
        typer.echo("Action non autorisée.")


# Gère la récupération des utilisateurs


# Affichage et sélection d'un client spécifique
def display_and_select_client(connected_user: User, filtered_clients):
    from controllers.menu_controller import navigate_client_options

    if not filtered_clients:
        typer.echo("Aucun client trouvé.")
        return

    selected_client_id = paginate_items(filtered_clients, display_clients, 10)
    if selected_client_id is None:
        return  # Gère le cas où l'utilisateur a pressé 'q' pour quitter

    with SessionLocal() as db:
        selected_client = db.query(Client).get(selected_client_id)
        if selected_client:
            typer.clear()
            display_client_profile(selected_client)
            navigate_client_options(connected_user, selected_client)


# Recherche de clients par nom
def handle_client_search_by_name(connected_user: User):
    db = SessionLocal()
    while True:  # Ajout d'une boucle pour permettre plusieurs tentatives
        try:
            last_name = typer.prompt(
                "Entrez le nom de famille du client à rechercher (q pour sortir de la recherche) ").lower()
            if last_name == "q":  # Permettre à l'utilisateur de sortir de la recherche
                return
            filtered_clients = db.query(Client).filter(Client.last_name.ilike(f"%{last_name}%")).all()

            if not filtered_clients:  # Si aucun client n'est trouvé
                typer.echo("Aucun client trouvé avec ce nom. Essayez à nouveau ou entrez 'q' pour quitter.")
                continue  # Revenir au prompt initial

            display_and_select_client(connected_user, filtered_clients)
        except Exception as e:
            typer.echo(f"Erreur lors de la recherche des clients: {e}")
        finally:
            db.close()  # Fermer la session après chaque utilisation


# Recherche de clients par commercial
def handle_client_search_by_commercial(connected_user: User):
    db = SessionLocal()
    try:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        if commercials:
            selected_commercial_id = paginate_items(commercials, display_users, 10)
            if selected_commercial_id:
                filtered_clients = db.query(Client).filter(Client.commercial_contact_id == selected_commercial_id).all()
                if filtered_clients:
                    display_and_select_client(connected_user, filtered_clients)
                else:
                    typer.echo("Aucun client trouvé pour ce commercial.")
        else:
            typer.echo("Aucun commercial trouvé.")
    except Exception as e:
        typer.echo(f"Erreur lors de la recherche de clients par commercial : {e}")
    finally:
        db.close()


# Listage de tous les clients
def handle_client_list_all_clients(connected_user: User):
    db = SessionLocal()
    try:
        all_clients = db.query(Client).options(joinedload(Client.commercial_contact)).all()
        if all_clients:
            display_and_select_client(connected_user, all_clients)
        else:
            typer.echo("Aucun client trouvé.")
    except Exception as e:
        typer.echo(f"Erreur lors du listage de tous les clients : {e}")
    finally:
        db.close()


# Gère la mise à jour d'un client
def update_client(connected_user: User, client_id: int):
    from controllers.menu_controller import navigate_client_menu
    if is_superuser(connected_user) or is_commerciale(connected_user):
        db = SessionLocal()
        client = db.query(Client).get(client_id)
        if not client:
            print("Client non trouvé.")
            return

        update_data = client_update_form(client)

        try:
            client.first_name = update_data.get("first_name", client.first_name)
            client.last_name = update_data.get("last_name", client.last_name)
            client.email = update_data.get("email", client.email)
            client.phone_number = update_data.get("phone_number", client.phone_number)
            client.company_name = update_data.get("company_name", client.company_name)
            client.commercial_contact_id = update_data.get('commercial_id', client.commercial_contact_id)

            db.commit()
            print("Client mis à jour avec succès.")
            display_client_profile(client)
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la mise à jour du client : {e}")
        finally:
            db.close()
    else:
        typer.echo("Action non autorisée.")
    navigate_client_menu(connected_user)


# Gère la suppression d'un client
def delete_client(connected_user, client_id: int):
    from controllers.menu_controller import navigate_client_menu
    if connected_user is is_superuser:
        db: Session = SessionLocal()
        client = db.query(Client).filter(Client.id == client_id).first()
        if client:
            db.delete(client)
            db.commit()
        db.close()
        typer.echo("Client supprimé avec succès.")
        navigate_client_menu(connected_user)
    else:
        typer.echo("Action non autorisée.")
