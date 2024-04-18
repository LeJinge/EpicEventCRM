# Exemple de test pytest
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, UserRole
from utils.security import pwd_context
from controllers.login_controller import app
from typer.testing import CliRunner

# Configuration de la base de données pour les tests
engine = create_engine('sqlite:///test.db')  # Utilisez une base de données appropriée pour les tests
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@pytest.fixture(scope="module")
def session():
    return SessionLocal()


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def setup_module(module):
    # Configurer les données initiales dans la base de données de test
    session = SessionLocal()
    hashed_password = pwd_context.hash("gestionpassword")
    user = User(email="gestion@exemple.com", password=hashed_password, role=UserRole.GESTION)
    session.add(user)
    session.commit()
    session.close()


def test_login_successful(runner, session):
    result = runner.invoke(app, ['login'], input="gestion@exemple.com\ngestionpassword\n")
    assert "Connexion réussie." in result.stdout


def test_login_failure(runner, session):
    result = runner.invoke(app, ['login'], input="gestion@exemple.com\nwrongpassword\n")
    assert "Échec de la connexion. Veuillez vérifier vos identifiants." in result.stdout
