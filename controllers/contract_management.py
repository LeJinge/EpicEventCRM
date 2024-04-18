import typer
from sqlalchemy.orm import Session

from models.models import Contract, UserRole, User, Client
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.permissions import is_superuser, is_gestion, is_commerciale
from utils.validation import validate_contract_data
from views.forms import contract_update_form, contract_form
from views.reports import display_contracts, display_users, display_clients, display_contract_profile


# Ajout d'un contrat
def add_contract(connected_user: User):
    from controllers.menu_controller import navigate_contract_menu
    db: Session = SessionLocal()
    try:
        # Collecter les données du contrat via un formulaire
        new_contract_data = contract_form()

        # Valider les données du contrat
        validate_contract_data(
            client_id=new_contract_data['client_id'],
            commercial_contact_id=new_contract_data['commercial_contact_id'],
            status=new_contract_data['status'],
            total_amount=new_contract_data['total_amount'],
            remaining_amount=new_contract_data['remaining_amount'],
            creation_date=new_contract_data['creation_date']
        )

        # Vérifier l'existence du client
        client = db.query(Client).filter(Client.id == new_contract_data['client_id']).first()
        if not client:
            raise ValueError("L'ID du client fourni ne correspond à aucun client existant.")

        # Vérifier l'existence du commercial
        commercial_user = db.query(User).filter(
            User.id == new_contract_data['commercial_contact_id'],
            User.role == UserRole.COMMERCIALE
        ).first()
        if not commercial_user:
            raise ValueError("L'ID commercial fourni ne correspond à aucun commercial valide.")

        # Création de l'objet Contract et sauvegarde en base de données
        new_contract = Contract(**new_contract_data)
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)
        db.close()

        typer.echo(f"Contrat ajouté avec succès.")

        return navigate_contract_menu(connected_user)
    except ValueError as e:
        db.rollback()
        typer.echo(f"Erreur: {e}")
    except Exception as e:
        db.rollback()
        typer.echo(f"Une erreur inattendue est survenue : {e}")
    finally:
        db.close()


# Affichage et sélection d'un contrat spécifique
def display_selected_contract_details(connected_user: User, filtered_contracts):
    from controllers.menu_controller import navigate_contract_options

    if not filtered_contracts:
        typer.echo("Aucun contrat trouvé.")
        return

    selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
    if selected_contract_id is None:
        return

    with SessionLocal() as db:
        selected_contract = db.query(Contract).get(selected_contract_id)
        if selected_contract:
            typer.clear()
            display_contract_profile(selected_contract)
            navigate_contract_options(connected_user, selected_contract)
        else:
            typer.echo("Contrat non trouvé.")


# Recherche de contrats par client
def handle_search_contract_by_client(connected_user: User):
    db = SessionLocal()
    try:
        clients = db.query(Client).all()
        selected_client_id = paginate_items(clients, display_clients, 10)
        if selected_client_id is not None:
            filtered_contracts = db.query(Contract).filter(Contract.client_id == selected_client_id).all()
            if filtered_contracts:
                display_selected_contract_details(connected_user, filtered_contracts)
            else:
                typer.echo("Aucun contrat trouvé pour ce client.")
    finally:
        db.close()


def handle_search_contract_by_commercial(connected_user: User):
    db = SessionLocal()
    try:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        selected_commercial_id = paginate_items(commercials, display_users, 10)
        if selected_commercial_id is not None:
            filtered_contracts = db.query(Contract).filter(
                Contract.commercial_contact_id == selected_commercial_id).all()
            if filtered_contracts:
                display_selected_contract_details(connected_user, filtered_contracts)
            else:
                typer.echo("Aucun contrat trouvé pour ce commercial.")
    finally:
        db.close()


def handle_search_contracts_in_progress(connected_user: User):
    db = SessionLocal()
    try:
        filtered_contracts = db.query(Contract).filter(Contract.status == "IN_PROGRESS").all()
        if filtered_contracts:
            display_selected_contract_details(connected_user, filtered_contracts)
        else:
            typer.echo("Aucun contrat en cours trouvé.")
    finally:
        db.close()


def handle_search_contracts_not_fully_paid(connected_user: User):
    with SessionLocal() as db:
        filtered_contracts = db.query(Contract).filter(Contract.remaining_amount > 0).all()
        if filtered_contracts:
            display_selected_contract_details(connected_user, filtered_contracts)
        else:
            typer.echo("Aucun contrat non entièrement payé trouvé.")


def handle_search_all_contracts(connected_user: User):
    with SessionLocal() as db:
        filtered_contracts = db.query(Contract).all()
        if filtered_contracts:
            display_selected_contract_details(connected_user, filtered_contracts)
        else:
            typer.echo("Aucun contrat trouvé.")


# Mise à jour d'un contrat
def update_contract(connected_user: User, contract_id):
    from controllers.menu_controller import navigate_contract_menu
    if is_superuser(connected_user) or is_gestion(connected_user) or is_commerciale(connected_user):
        db: Session = SessionLocal()
        contract = db.query(Contract).get(contract_id)
        if not contract:
            typer.echo("Contrat non trouvé.")
            db.close()
            return

        update_data = contract_update_form(contract)  # Vous devrez définir cette fonction

        try:
            contract.status = update_data.get("status", contract.status)
            contract.total_amount = update_data.get("total_amount", contract.total_amount)
            contract.remaining_amount = update_data.get("remaining_amount", contract.remaining_amount)
            contract.commercial_contact_id = update_data.get("commercial_contact_id", contract.commercial_contact_id)
            # Mettre à jour les données ici, similaire à la mise à jour d'un client
            db.commit()
            typer.clear()
            typer.echo("Contrat mis à jour avec succès.")
            display_contract_profile(contract)  # Vous devez définir cette fonction
            typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des contrats"...')
            navigate_contract_menu(connected_user)
        except Exception as e:
            db.rollback()
            typer.echo(f"Erreur lors de la mise à jour du contrat : {e}")
        finally:
            db.close()
    else:
        typer.echo("Accès non autorisé.")


# Suppression d'un contrat
def delete_contract(connected_user: User, contract_id):
    if is_superuser(connected_user):
        db: Session = SessionLocal()
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if contract:
            db.delete(contract)
            db.commit()
            typer.echo("Contrat supprimé avec succès.")
        else:
            typer.echo("Contrat non trouvé.")
        db.close()
    else:
        typer.echo("Action non autorisée.")
