from typing import Optional

import typer

from models.models import Client, User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.reports import display_clients, display_users


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
