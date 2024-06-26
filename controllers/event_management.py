import sentry_sdk
import typer
from sqlalchemy.orm import Session

from models.models import User, Event, Contract, UserRole, Client
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.permissions import is_superuser, is_gestion, is_support
from views.forms import event_form, event_update_form
from views.messages import event_not_found, action_not_authorised, add_event_success, update_event_success, \
    contract_not_found, delete_event_success
from views.reports import display_event_profile, display_contracts, display_events, display_users, display_clients


def add_event(connected_user: User):
    from controllers.menu_controller import navigate_event_menu
    db = SessionLocal()
    try:
        event_data = event_form()
        # validate_event_data(**event_data)

        new_event = Event(**event_data)
        db.add(new_event)
        db.commit()

        add_event_success()
        return navigate_event_menu(connected_user)  # Assurez-vous de définir cette fonction de navigation
    except Exception as e:
        sentry_sdk.capture_exception()
        db.rollback()
        typer.echo(f"Erreur lors de l'ajout de l'événement : {e}")
    finally:
        db.close()


def display_selected_event_details(connected_user: User, filtered_events):
    from controllers.menu_controller import navigate_event_options

    if not filtered_events:
        event_not_found()
        return

    selected_event_id = paginate_items(filtered_events, display_events, 10)
    if selected_event_id is None:
        return

    with SessionLocal() as db:
        event = db.query(Event).filter(Event.id == selected_event_id).first()
        if event:
            typer.clear()
            display_event_profile(event)
            navigate_event_options(connected_user, event)
        else:
            event_not_found()


def handle_search_event_by_contract(connected_user: User):
    db = SessionLocal()
    try:
        contracts = db.query(Contract).all()
        selected_contract_id = paginate_items(contracts, display_contracts, 10)
        if selected_contract_id:
            filtered_events = db.query(Event).filter(Event.contract_id == selected_contract_id).all()
            if filtered_events:
                display_selected_event_details(connected_user, filtered_events)
            else:
                event_not_found()
    finally:
        db.close()


def handle_search_event_by_support_contact(connected_user: User):
    db = SessionLocal()
    try:
        support_contacts = db.query(User).filter(User.role == UserRole.SUPPORT).all()
        selected_support_id = paginate_items(support_contacts, display_users, 10)
        if selected_support_id:
            filtered_events = db.query(Event).filter(Event.support_contact_id == selected_support_id).all()
            if filtered_events:
                display_selected_event_details(connected_user, filtered_events)
            else:
                event_not_found()
    finally:
        db.close()


def handle_search_event_without_support_contact(connected_user: User):
    db = SessionLocal()
    try:
        filtered_events = db.query(Event).filter(Event.support_contact_id == None).all()
        if filtered_events:
            display_selected_event_details(connected_user, filtered_events)
        else:
            event_not_found()
    finally:
        db.close()


def handle_search_event_by_client(connected_user: User):
    db = SessionLocal()
    try:
        clients = db.query(Client).all()
        selected_client_id = paginate_items(clients, display_clients, 10)
        if selected_client_id:
            filtered_events = db.query(Event).filter(Event.client_id == selected_client_id).all()
            if filtered_events:
                display_selected_event_details(connected_user, filtered_events)
        else:
            event_not_found()
    finally:
        db.close()


def handle_search_all_events(connected_user: User):
    db = SessionLocal()
    filtered_events = db.query(Event).all()
    if filtered_events:
        display_selected_event_details(connected_user, filtered_events)
    else:
        event_not_found()
    db.close()


def update_event(connected_user: User, event_id: int):
    from controllers.menu_controller import navigate_event_menu
    if is_superuser(connected_user) or is_gestion(connected_user) or is_support(connected_user):
        db: Session = SessionLocal()
        event = db.query(Event).get(event_id)
        if not event:
            event_not_found()
            return

        update_data = event_update_form(event)

        try:
            event.title = update_data.get("title", event.title)
            event.location = update_data.get("location", event.location)
            event.attendees = update_data.get("attendees", event.attendees)
            event.notes = update_data.get("notes", event.notes)
            event.start_date = update_data.get("start_date", event.start_date)
            event.end_date = update_data.get("end_date", event.end_date)
            event.support_contact_id = update_data.get("support_contact_id", event.support_contact_id)

            db.commit()
            update_event_success()
            display_event_profile(event)
            typer.pause('Appuyez sur Entrée pour continuer...')
            navigate_event_menu(connected_user)
        except Exception as e:
            sentry_sdk.capture_exception()
            db.rollback()
            typer.echo(f"Erreur lors de la mise à jour de l'événement : {e}")
        finally:
            event_not_found()
        db.close()
    else:
        action_not_authorised()


def delete_event(connected_user, event_id: int):
    if is_superuser(connected_user):
        db: Session = SessionLocal()
        event = db.query(Contract).filter(Event.id == event_id).first()
        if event:
            db.delete(event)
            db.commit()
            delete_event_success()
        else:
            contract_not_found()
        db.close()
    else:
        action_not_authorised()
