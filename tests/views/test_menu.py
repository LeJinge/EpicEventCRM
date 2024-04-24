# Supposons que votre modèle User soit défini avec un 'role' comme suit:
import pytest
from unittest.mock import patch
from views.menu import display_main_menu, display_user_management_menu, display_search_user_menu, display_user_options, \
    display_client_management_menu, display_search_client_menu, display_client_options, \
    display_contract_management_menu, display_search_contract_menu, display_contract_options, \
    display_event_management_menu, display_search_event_menu, display_event_options

from models.models import User


@pytest.fixture
def user_superuser(session):
    user = User(email="jeremy.carmona@exemple.com", role="SUPERUSER")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_gestion(session):
    user = User(email="gestion@exemple.com", role="GESTION")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_commerciale(session):
    user = User(email="commercial.user1@example.com", role="COMMERCIALE")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_support(session):
    user = User(email="support.user1@example.com", role="SUPPORT")
    session.add(user)
    session.commit()
    return user


def test_display_main_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_main_menu(user_superuser)
        mock_display.assert_called_once_with("Menu Principal", [
            "1. Recherche",
            "2. Gestion des collaborateurs",
            "3. Gestion des clients",
            "4. Gestion des contrats",
            "5. Gestion des évènements",
            "0. Quitter",
        ])


def test_display_main_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_main_menu(user_gestion)
        mock_display.assert_called_once_with("Menu Principal", [
            "1. Recherche",
            "2. Gestion des collaborateurs",
            "3. Gestion des contrats",
            "4. Gestion des évènements",
            "0. Quitter",
        ])


def test_display_main_menu_for_commerciale(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_main_menu(user_commerciale)
        mock_display.assert_called_once_with("Menu Principal", [
            "1. Recherche",
            "2. Gestion des clients",
            "3. Gestion des contrats",
            "4. Gestion des évènements",
            "0. Quitter",
        ])


def test_display_main_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_main_menu(user_support)
        mock_display.assert_called_once_with("Menu Principal", [
            "1. Recherche",
            "2. Gestion des évènements",
            "0. Quitter",
        ])


def test_display_user_management_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_user_management_menu(user_superuser)
        mock_display.assert_called_once_with("Gestion des Collaborateurs", [
            "1. Créer un collaborateur",
            "2. Rechercher un collaborateur",
            "0. Retour"
        ])


def test_display_user_management_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_user_management_menu(user_gestion)
        mock_display.assert_called_once_with("Gestion des Collaborateurs", [
            "1. Créer un collaborateur",
            "2. Rechercher un collaborateur",
            "0. Retour"
        ])


def test_display_user_management_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_user_management_menu(user_commerciale)
        # Vérifiez que display_menu est appelé avec les bons paramètres
        mock_display.assert_called_once_with("Gestion des Collaborateurs", ["Accès refusé."])


def test_display_user_management_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_user_management_menu(user_support)
        mock_display.assert_called_once_with("Gestion des Collaborateurs", ["Accès refusé."])


def test_display_search_user_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_search_user_menu(user_superuser)
        mock_display.assert_called_once_with("Recherche de Collaborateurs", [
            "1. Rechercher par nom",
            "2. Rechercher par équipe",
            "3. Tous les collaborateurs",
            "0. Retour"
        ])


def test_display_search_user_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_search_user_menu(user_gestion)
        mock_display.assert_called_once_with("Recherche de Collaborateurs", [
            "1. Rechercher par nom",
            "2. Rechercher par équipe",
            "3. Tous les collaborateurs",
            "0. Retour"
        ])


def test_display_search_user_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_search_user_menu(user_commerciale)
        mock_display.assert_called_once_with("Recherche de Collaborateurs", ["Accès refusé."])


def test_display_search_user_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_search_user_menu(user_support)
        mock_display.assert_called_once_with("Recherche de Collaborateurs", ["Accès refusé."])


def test_display_user_options_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_user_options(user_superuser)
        mock_display.assert_called_once_with("Options disponibles pour collaborateur", [
            "1. Modifier ce collaborateur",
            "2. Supprimer ce collaborateur",
            "0. Retour"
        ])


def test_display_user_options_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_user_options(user_gestion)
        mock_display.assert_called_once_with("Options disponibles pour collaborateur", [
            "1. Modifier ce collaborateur",
            "0. Retour"
        ])


def test_display_user_options_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_user_options(user_commerciale)
        mock_display.assert_called_once_with("Options disponibles pour collaborateur", ["Accès refusé."])


def test_display_user_options_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_user_options(user_support)
        mock_display.assert_called_once_with("Options disponibles pour collaborateur", ["Accès refusé."])


def test_display_client_management_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_client_management_menu(user_superuser)
        mock_display.assert_called_once_with("Gestion des Clients", [
            "1. Créer un client",
            "2. Rechercher un client",
            "0. Retour"
        ])


def test_display_client_management_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_client_management_menu(user_commerciale)
        mock_display.assert_called_once_with("Gestion des Clients", [
            "1. Créer un client",
            "2. Rechercher un client",
            "0. Retour"
        ])


def test_display_client_management_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_client_management_menu(user_support)
        mock_display.assert_called_once_with("Gestion des Clients", ["Accès refusé."])


def test_display_client_management_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_client_management_menu(user_gestion)
        mock_display.assert_called_once_with("Gestion des Clients", ["Accès refusé."])


def test_display_search_client_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_search_client_menu(user_superuser)
        mock_display.assert_called_once_with("Recherche de Clients", [
            "1. Rechercher par nom",
            "2. Rechercher par commercial",
            "3. Tous les clients",
            "0. Retour"
        ])


def test_display_search_client_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_search_client_menu(user_commerciale)
        mock_display.assert_called_once_with("Recherche de Clients", [
            "1. Rechercher par nom",
            "2. Rechercher par commercial",
            "3. Tous les clients",
            "0. Retour"
        ])


def test_display_search_client_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_search_client_menu(user_support)
        mock_display.assert_called_once_with("Recherche de Clients", ["Accès refusé."])


def test_display_search_client_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_search_client_menu(user_gestion)
        mock_display.assert_called_once_with("Recherche de Clients", ["Accès refusé."])


def test_display_client_options_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_client_options(user_superuser)
        mock_display.assert_called_once_with("Options disponibles pour ce client", [
            "1. Modifier ce client",
            "2. Supprimer ce client",
            "0. Retour"
        ])


def test_display_client_options_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_client_options(user_commerciale)
        mock_display.assert_called_once_with("Options disponibles pour ce client", [
            "1. Modifier ce client",
            "0. Retour",
        ])


def test_display_client_options_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_client_options(user_support)
        mock_display.assert_called_once_with("Options disponibles pour ce client", ["Accès refusé."])


def test_display_client_options_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_client_options(user_gestion)
        mock_display.assert_called_once_with("Options disponibles pour ce client", ["Accès refusé."])


def test_display_contract_management_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_management_menu(user_superuser)
        mock_display.assert_called_once_with("Gestion des Contrats", [
            "1. Créer un contrat",
            "2. Rechercher un contrat",
            "0. Retour"
        ])


def test_display_contract_management_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_management_menu(user_gestion)
        mock_display.assert_called_once_with("Gestion des Contrats", [
            "1. Créer un contrat",
            "2. Rechercher un contrat",
            "0. Retour"
        ])


def test_display_contract_management_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_management_menu(user_commerciale)
        mock_display.assert_called_once_with("Gestion des Contrats", [
            "1. Rechercher un contrat",
            "0. Retour",
        ])


def test_display_contract_management_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_management_menu(user_support)
        mock_display.assert_called_once_with("Gestion des Contrats", ["Accès refusé."])


def test_display_search_contract_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_search_contract_menu(user_superuser)
        mock_display.assert_called_once_with("Recherche de Contrats", [
            "1. Rechercher par client",
            "2. Rechercher par commercial",
            "3. Contrats en cours",
            "4. Contrats non entièrement payés",
            "5. Tous les contrats",
            "0. Retour",
        ])


def test_display_search_contract_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_search_contract_menu(user_gestion)
        mock_display.assert_called_once_with("Recherche de Contrats", [
            "1. Rechercher par client",
            "2. Rechercher par commercial",
            "3. Contrats en cours",
            "4. Contrats non entièrement payés",
            "5. Tous les contrats",
            "0. Retour",
        ])


def test_display_search_contract_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_search_contract_menu(user_commerciale)
        mock_display.assert_called_once_with("Recherche de Contrats", [
            "1. Rechercher par client",
            "2. Rechercher par commercial",
            "3. Contrats en cours",
            "4. Contrats non entièrement payés",
            "5. Tous les contrats",
            "0. Retour",
        ])


def test_display_search_contract_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_search_contract_menu(user_support)
        mock_display.assert_called_once_with("Recherche de Contrats", ["Accès refusé."])


def test_display_contract_options_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_options(user_superuser)
        mock_display.assert_called_once_with("Options disponibles pour ce contrat", [
            "1. Modifier ce contrat",
            "2. Supprimer ce contrat",
            "0. Retour"
        ])


def test_display_contract_options_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_options(user_gestion)
        mock_display.assert_called_once_with("Options disponibles pour ce contrat", ["0. Retour"])


def test_display_contract_options_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_options(user_commerciale)
        mock_display.assert_called_once_with("Options disponibles pour ce contrat", [
            "1. Modifier ce contrat",
            "0. Retour",
        ])


def test_display_contract_options_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_contract_options(user_support)
        mock_display.assert_called_once_with("Options disponibles pour ce contrat", ["0. Retour"])


def test_display_event_management_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_event_management_menu(user_superuser)
        mock_display.assert_called_once_with("Gestion des Évènements", [
            "1. Créer un évènement",
            "2. Rechercher un évènement",
            "0. Retour"
        ])


def test_display_event_management_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_event_management_menu(user_commerciale)
        mock_display.assert_called_once_with("Gestion des Évènements", [
            "1. Créer un évènement",
            "2. Rechercher un évènement",
            "0. Retour"
        ])


def test_display_event_management_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_event_management_menu(user_gestion)
        mock_display.assert_called_once_with("Gestion des Évènements", [
            "1. Rechercher un évènement",
            "0. Retour"
        ])


def test_display_event_management_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_event_management_menu(user_support)
        mock_display.assert_called_once_with("Gestion des Évènements", [
            "1. Rechercher un évènement",
            "0. Retour"
        ])


def test_display_search_event_menu_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_search_event_menu(user_superuser)
        mock_display.assert_called_once_with("Recherche d'Évènements", [
            "1. Rechercher par contrat",
            "2. Rechercher par support",
            "3. Évènements sans support",
            "4. Rechercher par client",
            "5. Tous les évènements",
            "0. Retour"
        ])


def test_display_search_event_menu_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_search_event_menu(user_commerciale)
        mock_display.assert_called_once_with("Recherche d'Évènements", [
            "1. Rechercher par contrat",
            "2. Rechercher par support",
            "3. Évènements sans support",
            "4. Rechercher par client",
            "5. Tous les évènements",
            "0. Retour"
        ])


def test_display_search_event_menu_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_search_event_menu(user_gestion)
        mock_display.assert_called_once_with("Recherche d'Évènements", [
            "1. Rechercher par contrat",
            "2. Rechercher par support",
            "3. Évènements sans support",
            "4. Rechercher par client",
            "5. Tous les évènements",
            "0. Retour"
        ])


def test_display_search_event_menu_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_search_event_menu(user_support)
        mock_display.assert_called_once_with("Recherche d'Évènements", [
            "1. Rechercher par contrat",
            "2. Rechercher par support",
            "3. Évènements sans support",
            "4. Rechercher par client",
            "5. Tous les évènements",
            "0. Retour"
        ])


def test_display_event_options_for_superuser(user_superuser):
    with patch('views.menu.display_menu') as mock_display:
        display_event_options(user_superuser)
        mock_display.assert_called_once_with("Options disponibles pour cet évènement", [
            "1. Modifier cet évènement",
            "2. Supprimer cet évènement",
            "0. Retour"
        ])


def test_display_event_options_for_gestion(user_gestion):
    with patch('views.menu.display_menu') as mock_display:
        display_event_options(user_gestion)
        mock_display.assert_called_once_with("Options disponibles pour cet évènement", [
            "1. Modifier cet évènement",
            "0. Retour"
        ])


def test_display_event_options_for_commercial(user_commerciale):
    with patch('views.menu.display_menu') as mock_display:
        display_event_options(user_commerciale)
        mock_display.assert_called_once_with("Options disponibles pour cet évènement", [
            "0. Retour"
        ])


def test_display_event_options_for_support(user_support):
    with patch('views.menu.display_menu') as mock_display:
        display_event_options(user_support)
        mock_display.assert_called_once_with("Options disponibles pour cet évènement", [
            "1. Modifier cet évènement",
            "0. Retour"
        ])
