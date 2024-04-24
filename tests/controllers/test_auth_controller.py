from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from controllers.auth_controller import authenticate_user
from controllers.login_controller import login
from models.models import User, UserRole, pwd_context
from views.login import get_user_credentials


@pytest.fixture
def runner():
    return CliRunner()


def test_authenticate_user(session):
    # Ajouter un utilisateur de test
    hashed_password = pwd_context.hash("gestionpassword")
    user = User(email="gestion@exemple.com", password=hashed_password, role=UserRole.GESTION)
    session.add(user)
    session.commit()

    # Tester l'authentification réussie
    authenticated_user = authenticate_user("gestion@exemple.com", "gestionpassword")
    assert authenticated_user is not None
    assert authenticated_user.email == "gestion@exemple.com"

    # Tester l'authentification échouée avec un mauvais mot de passe
    assert authenticate_user("gestion@exemple.com", "wrongpassword") is None


