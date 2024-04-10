import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, Session

from models.models import Contract, ContractStatus, Client, User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.validation import validate_contract_data
from views.forms import contract_form, contract_update_form
from views.menus import display_search_contract_menu, display_contract_management_menu, display_contract_options
from views.reports import display_contracts, display_contract_profile, display_clients, display_users


def handle_contract_management_menu():
    while True:
        typer.clear()
        display_contract_management_menu()
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent", type=int)

        if choice == 1:
            # Ajouter un client
            add_contract()
        elif choice == 2:
            # Rechercher un client
            contract_search_controller()
        elif choice == 0:
            break
        else:
            typer.echo("Choix invalide handle_client_management_menu.")
    return


# Gère l'ajout d'un nouveau contrat
def add_contract():
    contract_data = contract_form()

    try:
        validate_contract_data(**contract_data)
        with SessionLocal() as db:
            contract = Contract(
                client_id=contract_data['client_id'],
                commercial_contact_id=contract_data['commercial_contact_id'],
                status=contract_data['status'],
                total_amount=contract_data['total_amount'],
                remaining_amount=contract_data['remaining_amount'],
                creation_date=contract_data['creation_date'],
            )

            db.add(contract)
            db.commit()
            db.refresh(contract)

            typer.echo(f"Contrat créé avec succès : ID {contract.id}, pour le client ID {contract.client_id}.")
    except ValueError as e:
        typer.echo(f"Erreur: {e}")
    except Exception as e:
        typer.echo(f"Une erreur inattendue est survenue : {e}")


# Gère la recherche des contrats
def display_selected_contract_details(selected_contract_id):
    try:
        with SessionLocal() as db:
            selected_contract = db.query(Contract).options(
                joinedload(Contract.client),
                joinedload(Contract.commercial_contact)
            ).get(selected_contract_id)
            if selected_contract:
                typer.clear()
                display_contract_profile(selected_contract)
                action_choice = display_contract_options(
                    selected_contract)  # Assurez-vous que cette fonction retourne un choix valide
                if action_choice == 1:
                    # Modifier le contrat
                    update_contract_controller(selected_contract_id)
                elif action_choice == 2:
                    # Supprimer le contrat
                    if typer.confirm(
                            "Êtes-vous sûr de vouloir supprimer ce contrat ?"):  # Correction du message de confirmation
                        delete_contract_controller(selected_contract_id)
                        typer.echo(f"Le contrat ID {selected_contract_id} a été supprimé.")
            else:
                typer.echo("Erreur lors de la récupération des détails du contrat sélectionné.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


def contract_search_controller():
    typer.clear()
    display_search_contract_menu()
    choice = typer.prompt("Entrez votre choix (1-4): ", type=int)

    try:
        with SessionLocal() as db:
            base_query = db.query(Contract).options(joinedload(Contract.client),
                                                    joinedload(Contract.commercial_contact))

            if choice == 1:
                handle_search_by_client(db, base_query)
            elif choice == 2:
                handle_search_by_commercial(db, base_query)
            elif choice == 3:
                handle_search_by_status(db, base_query)
            elif choice == 4:
                handle_list_all_contracts(db, base_query)
            else:
                typer.echo("Choix invalide.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


def handle_search_by_client(db, base_query):
    clients = db.query(Client).all()
    if clients:
        selected_client_id = paginate_items(clients, display_clients, 10)
        if selected_client_id:
            filtered_contracts = base_query.filter(Contract.client_id == selected_client_id).all()
            if filtered_contracts:
                selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
                if selected_contract_id:
                    display_selected_contract_details(selected_contract_id)
            else:
                typer.echo("Aucun contrat trouvé pour ce client.")
    else:
        typer.echo("Aucun client trouvé.")


def handle_search_by_commercial(db, base_query):
    commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
    if commercials:
        selected_commercial_id = paginate_items(commercials, display_users, 10)
        if selected_commercial_id:
            filtered_contracts = base_query.filter(Contract.commercial_contact_id == selected_commercial_id).all()
            if filtered_contracts:
                selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
                if selected_contract_id:
                    display_selected_contract_details(selected_contract_id)
            else:
                typer.echo("Aucun contrat trouvé pour ce commercial.")
        else:
            typer.echo("Aucun commercial sélectionné.")
    else:
        typer.echo("Aucun commercial trouvé.")


def handle_search_by_status(db, base_query):
    typer.echo("Choisissez un statut de contrat:")
    for idx, status in enumerate(ContractStatus, start=1):
        typer.echo(f"{idx}. {status.value}")
    status_choice = typer.prompt("Entrez votre choix: ", type=int)
    if 1 <= status_choice <= len(ContractStatus):
        selected_status = list(ContractStatus)[status_choice - 1]
        filtered_contracts = base_query.filter(Contract.status == selected_status).all()
        if filtered_contracts:
            selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
            if selected_contract_id:
                display_selected_contract_details(selected_contract_id)
        else:
            typer.echo(f"Aucun contrat trouvé avec le statut '{selected_status.value}'.")
    else:
        typer.echo("Choix de statut invalide.")


def handle_list_all_contracts(db, base_query):
    all_contracts = base_query.all()
    if all_contracts:
        selected_contract_id = paginate_items(all_contracts, display_contracts, 10)
        if selected_contract_id:
            display_selected_contract_details(selected_contract_id)
        else:
            typer.echo("Aucun contrat sélectionné.")
    else:
        typer.echo("Aucun contrat trouvé.")


# Gère la modification d'un contrat

def update_contract_controller(contract_id: int):
    db: Session = SessionLocal()
    try:
        contract = db.query(Contract).get(contract_id)
        if not contract:
            typer.echo("Contrat non trouvé.")
            return

        update_data = contract_update_form(contract)

        # Mise à jour du statut si nécessaire
        if 'status' in update_data:
            try:
                update_data['status'] = ContractStatus(
                    update_data['status'].upper())  # Assurez-vous que la valeur est dans l'énumération
            except KeyError:
                typer.echo("Statut de contrat invalide.")
                return

        # Mise à jour de l'ID du contact commercial si nécessaire
        if 'commercial_contact_id' in update_data and update_data['commercial_contact_id']:
            update_data['commercial_contact_id'] = int(update_data['commercial_contact_id'])

        # Appliquer les mises à jour
        for key, value in update_data.items():
            if hasattr(contract, key):
                setattr(contract, key, value)

        db.commit()
        typer.echo(f"Contrat ID {contract.id} mis à jour avec succès.")
        display_contract_profile(contract)
        typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des clients"...')
    except Exception as e:
        db.rollback()  # Assurez-vous de faire un rollback en cas d'erreur
        typer.echo(f"Une erreur inattendue est survenue : {e}")
    finally:
        db.close()


# Gère la modification d'un contrat
def delete_contract_controller(contract_id: int):
    db: Session = SessionLocal()
    try:
        contract = db.query(Contract).get(contract_id)
        if not contract:
            typer.echo("Contrat non trouvé.")
            return

        db.delete(contract)
        db.commit()
    except Exception as e:
        db.rollback()
        typer.echo(f"Une erreur inattendue est survenue : {e}")
    finally:
        db.close()
