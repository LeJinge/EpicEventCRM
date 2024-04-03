from models.models import UserRole


def is_superuser(user_role) -> bool:
    return user_role == UserRole.SUPERUSER


def is_gestion(user_role) -> bool:
    return user_role == UserRole.GESTION


def is_commerciale(user_role) -> bool:
    return user_role == UserRole.COMMERCIALE


def is_support(user_role) -> bool:
    return user_role == UserRole.SUPPORT
