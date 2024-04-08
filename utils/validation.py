import re

from models.models import UserRole


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
