import traceback
import typer
from sqlalchemy.orm import Session, joinedload

from models.models import Client, User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.validation import validate_client_data
from views.forms import client_form, client_update_form
from views.reports import display_client_profile, display_clients, display_users


# Gère l'ajout d'un nouveau client
def add_client(user: User):
    from controllers.menu_controller import navigate_client_menu
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
        return navigate_client_menu(user)
    except ValueError as e:
        typer.echo(f"Erreur: {e}")
    except Exception as e:
        typer.echo(f"Une erreur inattendue est survenue : {e}")


# Gère la récupération des utilisateurs


# Affichage et sélection d'un client spécifique
def display_and_select_client(user: User, filtered_clients, db):
    from controllers.menu_controller import navigate_client_options
    if filtered_clients:
        selected_client_id = paginate_items(filtered_clients, display_clients, 10)
        if selected_client_id:
            selected_client = db.query(Client).get(selected_client_id)
            typer.clear()
            display_client_profile(selected_client)  # Affiche le profil du client sélectionné
            navigate_client_options(user, selected_client)
    else:
        typer.echo("Aucun client trouvé.")


# Recherche de clients par nom
def handle_client_search_by_name(user: User):
    db = SessionLocal()
    try:
        name = typer.prompt("Entrez le nom de famille du client à rechercher: ").lower()
        filtered_clients = db.query(Client).filter(Client.last_name.ilike(f"%{name}%")).all()
        display_and_select_client(user, filtered_clients, db)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Erreur lors de la recherche des clients: {e}")
    finally:
        db.close()


# Recherche de clients par commercial
def handle_client_search_by_commercial(user: User):
    db = SessionLocal()
    try:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        if commercials:
            selected_commercial_id = paginate_items(commercials, display_users, 10)
            if selected_commercial_id:
                filtered_clients = db.query(Client).filter(Client.commercial_contact_id == selected_commercial_id).all()
                if filtered_clients:
                    display_and_select_client(user, filtered_clients, db)
                else:
                    typer.echo("Aucun client trouvé pour ce commercial.")
        else:
            typer.echo("Aucun commercial trouvé.")
    except Exception as e:
        typer.echo(f"Erreur lors de la recherche de clients par commercial : {e}")
    finally:
        db.close()


# Listage de tous les clients
def handle_client_list_all_clients(user: User):
    db = SessionLocal()
    try:
        all_clients = db.query(Client).options(joinedload(Client.commercial_contact)).all()
        if all_clients:
            display_and_select_client(user, all_clients, db)
        else:
            typer.echo("Aucun client trouvé.")
    except Exception as e:
        typer.echo(f"Erreur lors du listage de tous les clients : {e}")
    finally:
        db.close()


# Gère la mise à jour d'un client
def update_client(user: User, client_id: int):
    from controllers.menu_controller import navigate_client_menu
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
        navigate_client_menu(user)
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la mise à jour du client : {e}")
    finally:
        db.close()


# Gère la suppression d'un client
def delete_client(client_id: int):
    from controllers.menu_controller import navigate_client_menu
    db: Session = SessionLocal()
    user = db.query(Client).filter(Client.id == client_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    typer.echo("Client supprimé avec succès.")
    navigate_client_menu(user)
