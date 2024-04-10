import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.functions import user

from models.models import Client, User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.validation import validate_client_data
from views.forms import client_form, client_update_form
from views.menus import display_client_management_menu, display_search_client_menu, display_client_options
from views.reports import display_client_profile, display_clients, display_users


def handle_client_management_menu():
    while True:
        typer.clear()
        display_client_management_menu(user)
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent: ", type=int)

        if choice == 1:
            # Ajouter un client
            add_client()
        elif choice == 2:
            # Rechercher un client
            client_search_controller()
        elif choice == 0:
            break
        else:
            typer.echo("Choix invalide handle_client_management_menu.")
    return


# Gère l'ajout d'un nouveau client
def add_client():
    client_data = client_form()
    try:
        validate_client_data()

        db: Session = SessionLocal()
        client = Client(
            first_name=client_data['first_name'],
            last_name=client_data['last_name'],
            email=client_data['email'],
            phone_number=client_data['phone_number'],
            company_name=client_data['company_name'],
            commercial_contact_id=client_data.get('commercial_id')
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        db.close()

        typer.echo(f"Client {client.first_name} {client.last_name} créé avec succès.")
    except ValueError as e:
        typer.echo(f"Erreur: {e}")
    except Exception as e:
        typer.echo(f"Une erreur inattendue est survenue : {e}")


# Gère la récupération des utilisateurs


def display_selected_client_details(selected_client_id):
    try:
        with SessionLocal() as db:
            selected_client = db.query(Client).options(
                joinedload(Client.commercial_contact)
            ).get(selected_client_id)
            if selected_client:
                typer.clear()
                display_client_profile(selected_client)
                action_choice = display_client_options(selected_client)
                if action_choice == 1:
                    # Modifier le client
                    update_client_controller(selected_client_id)
                elif action_choice == 2:
                    # Supprimer le client
                    if typer.confirm("Êtes-vous sûr de vouloir supprimer ce client ?"):
                        delete_client_controller(selected_client_id)
                        typer.echo(
                            f"Le client {selected_client.first_name} {selected_client.last_name} a été supprimé.")
            else:
                typer.echo("Erreur lors de la récupération des détails du client sélectionné.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


def client_search_controller():
    typer.clear()
    display_search_client_menu()
    choice = typer.prompt("Entrez votre choix (1-3): ", type=int)

    try:
        with SessionLocal() as db:
            clients = db.query(Client).options(joinedload(Client.commercial_contact)).all()

            if choice == 1:  # Recherche par nom
                handle_search_by_name(db)
            elif choice == 2:  # Recherche par commercial
                handle_search_by_commercial_client(db)
            elif choice == 3:  # Afficher tous les clients
                handle_list_all_clients(db)
            else:
                typer.echo("Choix invalide.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


def handle_search_by_name(db):
    name = typer.prompt("Entrez le nom de famille du client à rechercher: ").lower()
    filtered_clients = [client for client in db.query(Client).options(joinedload(Client.commercial_contact)).all() if
                        name in client.last_name.lower()]
    if filtered_clients:
        selected_client_id = paginate_items(filtered_clients, display_clients, 10)
        if selected_client_id:
            display_selected_client_details(selected_client_id)
    else:
        typer.echo("Aucun client trouvé avec ce nom.")


def handle_search_by_commercial_client(db):
    commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
    if commercials:
        selected_commercial_id = paginate_items(commercials, display_users, 10)
        if selected_commercial_id:
            filtered_clients = [client for client in
                                db.query(Client).options(joinedload(Client.commercial_contact)).all() if
                                client.commercial_contact_id == selected_commercial_id]
            if filtered_clients:
                selected_client_id = paginate_items(filtered_clients, display_clients, 10)
                if selected_client_id:
                    display_selected_client_details(selected_client_id)
            else:
                typer.echo("Aucun client trouvé pour ce commercial.")
    else:
        typer.echo("Aucun commercial trouvé.")


def handle_list_all_clients(db):
    all_clients = db.query(Client).options(joinedload(Client.commercial_contact)).all()
    if all_clients:
        selected_client_id = paginate_items(all_clients, display_clients, 10)
        if selected_client_id:
            display_selected_client_details(selected_client_id)
    else:
        typer.echo("Aucun client trouvé.")


# Gère la mise à jour d'un client
def update_client_controller(client_id: int):
    db: Session = SessionLocal()
    client = db.query(Client).get(client_id)
    if not client:
        print("Client non trouvé.")
        db.close()
        return

    update_data = client_update_form(client)

    try:
        if 'commercial_id' not in update_data:  # Si commercial_id est optionnel
            update_data['commercial_id'] = None

        # Mise à jour des informations du client
        client.first_name = update_data["first_name"]
        client.last_name = update_data["last_name"]
        client.email = update_data["email"]
        client.phone_number = update_data["phone_number"]
        client.company_name = update_data["company_name"]

        # Mise à jour de l'ID commercial_contact seulement si un commercial_id valide est fourni
        if update_data['commercial_id'] is not None:
            if db.query(User).filter(User.id == update_data['commercial_id'],
                                     User.role == UserRole.COMMERCIALE).one_or_none():
                client.commercial_contact_id = update_data['commercial_id']
            else:
                print("Aucun commercial correspondant à l'ID fourni.")

        db.commit()
        typer.clear()
        print("Client mis à jour avec succès.")
        display_client_profile(client)
        typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des clients"...')
        return
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la mise à jour du client : {e}")
    finally:
        db.close()


# Gère la suppression d'un client
def delete_client_controller(client_id: int):
    db: Session = SessionLocal()
    user = db.query(Client).filter(Client.id == client_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()