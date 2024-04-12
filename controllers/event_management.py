import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, Session

from models.models import User, Event, Contract, UserRole, Client
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.validation import validate_event_data
from views.forms import event_form, event_update_form
from views.reports import display_event_profile, display_contracts, display_events, display_users, display_clients


def add_event(user: User):
    from controllers.menu_controller import navigate_event_menu
    db = SessionLocal()
    try:
        event_data = event_form()  # Assurez-vous que cette fonction recueille toutes les données nécessaires
        validate_event_data(**event_data)

        new_event = Event(**event_data)
        db.add(new_event)
        db.commit()

        typer.echo("Événement ajouté avec succès.")
        return navigate_event_menu(user)  # Assurez-vous de définir cette fonction de navigation
    except Exception as e:
        db.rollback()
        typer.echo(f"Erreur lors de l'ajout de l'événement : {e}")
    finally:
        db.close()


def display_selected_event_details(user: User, event_id):
    from controllers.menu_controller import navigate_event_options
    try:
        with SessionLocal() as db:
            selected_event = db.query(Event).options(
                joinedload(Event.contract),
                joinedload(Event.support_contact)
            ).get(event_id)
            if selected_event:
                typer.clear()
                display_event_profile(selected_event)
                navigate_event_options(user, selected_event)
            else:
                typer.echo("Erreur lors de la récupération des détails de l'événement sélectionné.")
    except SQLAlchemyError as e:
        typer.echo(f"Une erreur de base de données est survenue : {e}")


def handle_search_event_by_contract(user: User):
    db = SessionLocal()
    contracts = db.query(Contract).all()
    selected_contract_id = paginate_items(contracts, display_contracts, 10)
    if selected_contract_id:
        filtered_events = db.query(Event).filter(Event.contract_id == selected_contract_id).all()
        if filtered_events:
            selected_event_id = paginate_items(filtered_events, display_events, 10)
            if selected_event_id:
                display_selected_event_details(user, selected_event_id)
        else:
            typer.echo("Aucun événement trouvé pour ce contrat.")
    db.close()


def handle_search_event_by_support_contact(user: User):
    db = SessionLocal()
    support_contacts = db.query(User).filter(User.role == UserRole.SUPPORT).all()
    selected_support_id = paginate_items(support_contacts, display_users, 10)
    if selected_support_id:
        filtered_events = db.query(Event).filter(Event.support_contact_id == selected_support_id).all()
        if filtered_events:
            selected_event_id = paginate_items(filtered_events, display_events, 10)
            if selected_event_id:
                display_selected_event_details(user, selected_event_id)
        else:
            typer.echo("Aucun événement trouvé pour ce contact de support.")
    db.close()


def handle_search_event_without_support_contact(user: User):
    db = SessionLocal()
    filtered_events = db.query(Event).filter(Event.support_contact_id == None).all()
    if filtered_events:
        selected_event_id = paginate_items(filtered_events, display_events, 10)
        if selected_event_id:
            display_selected_event_details(user, selected_event_id)
    else:
        typer.echo("Aucun événement trouvé sans contact de support.")
    db.close()


def handle_search_event_by_client(user: User):
    db = SessionLocal()
    clients = db.query(Client).all()
    selected_client_id = paginate_items(clients, display_clients, 10)
    if selected_client_id:
        filtered_events = db.query(Event).filter(Event.client_id == selected_client_id).all()
        if filtered_events:
            selected_event_id = paginate_items(filtered_events, display_events, 10)
            if selected_event_id:
                display_selected_event_details(user, selected_event_id)
    else:
        typer.echo("Aucun événement trouvé pour ce client.")
    db.close()


def handle_search_all_events(user: User):
    db = SessionLocal()
    all_events = db.query(Event).all()
    if all_events:
        selected_event_id = paginate_items(all_events, display_events, 10)
        if selected_event_id:
            display_selected_event_details(user, selected_event_id)
    else:
        typer.echo("Aucun événement trouvé.")
    db.close()


def update_event(event_id: int):
    db: Session = SessionLocal()
    event = db.query(Event).get(event_id)
    if event:
        update_data = event_update_form(event)  # Assurez-vous que cette fonction recueille toutes les données mises à jour
        # Mettez à jour l'objet event ici avec les nouvelles valeurs
        db.commit()
        typer.echo("Événement mis à jour avec succès.")
    else:
        typer.echo("Événement non trouvé.")
    db.close()


def delete_event(event_id: int):
    db: Session = SessionLocal()
    event = db.query(Contract).filter(Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        typer.echo("Contrat supprimé avec succès.")
    else:
        typer.echo("Contrat non trouvé.")
    db.close()
