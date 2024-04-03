import re

from models.models import UserRole


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


# Valide les données de l'utilisateur avant la création
def validate_user_data(first_name: str, last_name, email: str, role_str: str, password: str):
    # Validation de l'email (exemple simple)
    if "@" not in email or "." not in email:
        raise ValueError("Email invalide.")

    # Vérifier que le rôle (sous forme de chaîne) est valide
    if role_str.upper() not in UserRole.__members__:
        raise ValueError(f"Rôle '{role_str}' invalide.")

    # Plus de validations peuvent être ajoutées ici...

    return True
