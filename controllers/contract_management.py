from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from models.models import Contract, UserRole, User, Client
from utils.db import SessionLocal
import typer

from utils.pagination import paginate_items
from utils.validation import validate_contract_data
from views.forms import contract_update_form, contract_form
from views.reports import display_contracts, display_users, display_clients, display_contract_profile


# Ajout d'un contrat
def add_contract(user: User):
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

        return navigate_contract_menu(user)
    except ValueError as e:
        db.rollback()
        typer.echo(f"Erreur: {e}")
    except Exception as e:
        db.rollback()
        typer.echo(f"Une erreur inattendue est survenue : {e}")
    finally:
        db.close()


# Affichage et sélection d'un contrat spécifique
def display_selected_contract_details(user: User, contract_id):
    from controllers.menu_controller import navigate_contract_options
    try:
        with SessionLocal() as db:
            selected_contract = db.query(Contract).options(
                joinedload(Contract.commercial_contact),
                joinedload(Contract.client)
            ).get(contract_id)
            if selected_contract:
                typer.clear()
                display_contract_profile(selected_contract)  # Affiche le profil du contrat sélectionné
                navigate_contract_options(user, selected_contract)
            else:
                typer.echo("Erreur lors de la récupération des détails du contrat sélectionné.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


# Recherche de contrats par client
def handle_search_contract_by_client(user: User):
    with SessionLocal() as db:
        clients = db.query(Client).all()
        selected_client_id = paginate_items(clients, display_clients, 10)
        if selected_client_id is not None:
            filtered_contracts = db.query(Contract).filter(Contract.client_id == selected_client_id).all()
            if filtered_contracts:
                selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
                if selected_contract_id:
                    display_selected_contract_details(user, selected_contract_id)
            else:
                typer.echo("Aucun contrat trouvé pour ce client.")


def handle_search_contract_by_commercial(user: User):
    with SessionLocal() as db:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        selected_commercial_id = paginate_items(commercials, display_users, 10)
        if selected_commercial_id is not None:
            filtered_contracts = db.query(Contract).filter(
                Contract.commercial_contact_id == selected_commercial_id).all()
            if filtered_contracts:
                selected_contract_id = paginate_items(filtered_contracts, display_contracts, 10)
                if selected_contract_id:
                    display_selected_contract_details(user, selected_contract_id)
            else:
                typer.echo("Aucun contrat trouvé pour ce commercial.")


def handle_search_all_contracts(user: User):
    with SessionLocal() as db:
        all_contracts = db.query(Contract).all()
        if all_contracts:
            selected_contract_id = paginate_items(all_contracts, display_contracts, 10)
            if selected_contract_id:
                display_selected_contract_details(user, selected_contract_id)
        else:
            typer.echo("Aucun contrat trouvé.")


# Mise à jour d'un contrat
def update_contract(contract_id):
    db: Session = SessionLocal()
    contract = db.query(Contract).get(contract_id)
    if not contract:
        typer.echo("Contrat non trouvé.")
        db.close()
        return

    update_data = contract_update_form(contract)  # Vous devrez définir cette fonction

    try:
        # Mettre à jour les données ici, similaire à la mise à jour d'un client
        db.commit()
        typer.clear()
        typer.echo("Contrat mis à jour avec succès.")
        display_contract_profile(contract)  # Vous devez définir cette fonction
        typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des contrats"...')
    except Exception as e:
        db.rollback()
        typer.echo(f"Erreur lors de la mise à jour du contrat : {e}")
    finally:
        db.close()


# Suppression d'un contrat
def delete_contract(contract_id):
    db: Session = SessionLocal()
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        db.delete(contract)
        db.commit()
        typer.echo("Contrat supprimé avec succès.")
    else:
        typer.echo("Contrat non trouvé.")
    db.close()
