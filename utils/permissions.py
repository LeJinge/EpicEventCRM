from models.models import User, UserRole


def is_superuser(user: User) -> bool:
    return user.role == UserRole.SUPERUSER


def is_gestion(user: User) -> bool:
    return user.role == UserRole.GESTION


def is_commerciale(user: User) -> bool:
    return user.role == UserRole.COMMERCIALE


def is_support(user: User) -> bool:
    return user.role == UserRole.SUPPORT
