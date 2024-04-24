import re
from datetime import datetime

import sentry_sdk

from models.models import UserRole, ContractStatus


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_user_data(first_name: str, last_name: str, email: str, role_str: str, password: str):
    if not first_name or not last_name:
        raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
    if not is_valid_email(email):
        raise ValueError("Email invalide.")
    if role_str.upper() not in UserRole.__members__:
        raise ValueError(f"Rôle '{role_str}' invalide.")
    return True


def validate_client_data(first_name: str, last_name: str, email: str, phone_number: str, company_name: str, **kwargs):
    if not first_name or not last_name:
        raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
    if not is_valid_email(email):
        raise ValueError("Email invalide.")
    if not re.match(r"^\+?\d[\d -]{7,14}\d$", phone_number):
        raise ValueError("Numéro de téléphone invalide.")
    if not company_name:
        raise ValueError("Le nom de l'entreprise ne peut pas être vide.")
    return True


def validate_contract_data(client_id: int, commercial_contact_id: int, status: str, total_amount: int,
                           remaining_amount: int, creation_date: str, **kwargs):
    if not client_id:
        raise ValueError("L'ID du client ne peut pas être vide.")
    if not commercial_contact_id:
        raise ValueError("L'ID du contact commercial ne peut pas être vide.")
    if status not in [status.value for status in ContractStatus]:
        raise ValueError("Statut de contrat invalide.")
    if total_amount < 0:
        raise ValueError("Le montant total ne peut pas être négatif.")
    if remaining_amount < 0:
        raise ValueError("Le montant restant ne peut pas être négatif.")
    if total_amount < remaining_amount:
        raise ValueError("Le montant restant ne peut pas être supérieur au montant total.")

    # Validation de la date de création
    try:
        creation_date_obj = datetime.strptime(creation_date, "%Y-%m-%d")
        if creation_date_obj > datetime.now():
            raise ValueError("La date de création ne peut pas être dans le futur.")
    except ValueError as e:
        sentry_sdk.capture_exception()
        raise ValueError(f"Format de la date de création invalide. Utilisez YYYY-MM-DD. Détail de l'erreur : {e}")

    return True


def validate_event_data():
    pass
