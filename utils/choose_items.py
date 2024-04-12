from typing import Optional

import typer

from models.models import Client, User, UserRole, Contract
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.reports import display_clients, display_users, display_contracts


def choose_client() -> Optional[int]:
    with SessionLocal() as db:
        clients = db.query(Client).all()
        if not clients:
            typer.echo("Aucun client trouvé.")
            return None

        selected_client_id = paginate_items(clients, display_clients, 10)
        return selected_client_id


def choose_commercial() -> Optional[int]:
    with SessionLocal() as db:
        commercials = db.query(User).filter(User.role == UserRole.COMMERCIALE).all()
        if not commercials:
            print("Aucun contact commercial trouvé.")
            return None

        selected_commercial_id = paginate_items(commercials, display_users, 10)

        return selected_commercial_id


def choose_contract() -> Optional[int]:
    with SessionLocal() as db:
        contracts = db.query(Contract).all()
        if not contracts:
            typer.echo("Aucun contrat trouvé.")
            return None

        selected_contract_id = paginate_items(contracts, display_contracts, 10)
        return selected_contract_id


def choose_support_contact() -> Optional[int]:
    with SessionLocal() as db:
        support_contacts = db.query(User).filter(User.role == UserRole.SUPPORT).all()
        if not support_contacts:
            typer.echo("Aucun contact de support trouvé.")
            return None

        selected_support_contact_id = paginate_items(support_contacts, display_users, 10)
        return selected_support_contact_id
