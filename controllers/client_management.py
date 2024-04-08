import typer
from sqlalchemy.orm import Session, joinedload

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
        display_client_management_menu()
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
    client_data = client_form()  # Supposons que cela récupère les données de l'utilisateur d'une manière ou d'une autre
    try:
        validate_client_data(**client_data)

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


def client_search_controller():
    typer.clear()
    display_search_client_menu()
    choice = typer.prompt("Entrez votre choix (1-3): ", type=int)

    with SessionLocal() as db:  # Assurez-vous que SessionLocal est correctement importé et configuré
        clients = db.query(Client).options(joinedload(Client.commercial_contact)).all()

        if choice == 1:  # Recherche par nom
            name = typer.prompt("Entrez le nom de famille du client à rechercher: ").lower()
            filtered_clients = [client for client in clients if name in client.last_name.lower()]
        elif choice == 2:  # Recherche par commercial
            commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
            if commercials:
                selected_commercial_id = paginate_items(commercials, display_users)  # Assurez-vous que display_commercials est correctement définie
                if selected_commercial_id:
                    filtered_clients = [client for client in clients if client.commercial_contact_id == selected_commercial_id]
                else:
                    filtered_clients = []
            else:
                typer.echo("Aucun commercial trouvé.")
                return
        elif choice == 3:  # Afficher tous les clients
            filtered_clients = clients
        else:
            typer.echo("Choix invalide.")
            return

        if filtered_clients:
            selected_client_id = paginate_items(filtered_clients, display_clients)
            if selected_client_id:
                selected_client = db.query(Client).get(selected_client_id)
                if selected_client:
                    display_client_profile(selected_client)
                    action_choice = display_client_options(selected_client)
                    if action_choice == 1:
                        update_client_controller(selected_client.id)
                    elif action_choice == 2:
                        if typer.confirm("Êtes-vous sûr de vouloir supprimer ce client ?"):
                            delete_client_controller(selected_client.id)
                            typer.echo(f"Le client {selected_client.first_name} {selected_client.last_name} a été supprimé.")
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
