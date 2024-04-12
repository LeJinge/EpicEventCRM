import typer

from controllers.client_management import add_client, update_client, delete_client, \
    handle_client_search_by_name, handle_client_search_by_commercial, handle_client_list_all_clients
from controllers.contract_management import add_contract, handle_search_contract_by_client, \
    handle_search_contract_by_commercial, handle_search_all_contracts
from controllers.event_management import add_event, update_event, \
    handle_search_event_by_contract, handle_search_event_by_support_contact, \
    handle_search_event_without_support_contact, handle_search_event_by_client, handle_search_all_events, delete_event
from controllers.logout_controller import logout
from controllers.user_management import add_user, handle_search_by_name, handle_search_by_role, handle_list_all_users, \
    update_user, delete_user
from models.models import User, Client, Event
from utils.db import SessionLocal
from utils.permissions import is_superuser, is_gestion, is_commerciale, is_support
from views.menu import display_main_menu, display_contract_management_menu, display_event_management_menu, \
    display_client_management_menu, display_search_user_menu, display_user_management_menu, display_user_options, \
    display_search_client_menu, display_client_options, display_search_menu, display_search_contract_menu, \
    display_contract_options, display_event_options, display_search_event_menu


def navigate_main_menus(user: User):
    display_main_menu(user)
    try:
        choice = int(input("Entrez votre choix ou 0 pour quitter: "))
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return navigate_main_menus(user)

    if choice == 0:
        logout()
    elif choice == 1:
        navigate_search_menu(user)
    else:
        if is_superuser(user):
            if choice == 2:
                navigate_user_menu(user)
            elif choice == 3:
                navigate_client_menu(user)
            elif choice == 4:
                navigate_contract_menu(user)
            elif choice == 5:
                navigate_event_menu(user)
        elif is_gestion(user):
            if choice == 2:
                navigate_user_menu(user)
            elif choice == 3:
                navigate_contract_menu(user)
            elif choice == 4:
                navigate_event_menu(user)
        elif is_commerciale(user):
            if choice == 2:
                navigate_client_menu(user)
            elif choice == 3:
                navigate_contract_menu(user)
            elif choice == 4:
                navigate_event_menu(user)
        elif is_support(user):
            if choice == 2:
                navigate_event_menu(user)
        else:
            print("Choix invalide, veuillez réessayer.")
            return navigate_main_menus(user)


def navigate_user_menu(user: User):
    display_user_management_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                add_user(user)
            elif choice == 2:
                navigate_user_search_menu(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_main_menus(user)


def navigate_user_search_menu(user: User):
    display_search_user_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input("Entrez votre choix ou 0 pour quitter: "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        if choice == 0:
            break
        else:
            with SessionLocal() as db:
                if choice == 1:
                    handle_search_by_name(db)
                elif choice == 2:
                    handle_search_by_role(db)
                elif choice == 3:
                    handle_list_all_users(db)
                else:
                    print("Choix invalide, veuillez réessayer.")
    navigate_user_menu(user)


def navigate_user_options(user: User):
    display_user_options(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_user(user.id)
            elif choice == 2:
                delete_user(user.id)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_user_menu(user)


def navigate_search_menu(user: User):
    display_search_menu()
    while True:
        try:
            choice = typer.prompt("Entrez votre choix (1-4): ", type=int)

            if choice == 1:
                navigate_user_search_menu(user),
            elif choice == 2:
                navigate_client_search_menu(user),
            elif choice == 3:
                navigate_contract_menu(user),
            elif choice == 4:
                navigate_event_menu(user),
            elif choice == 0:
                break
            else:  # Choix invalide
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def navigate_client_menu(user: User):
    display_client_management_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                add_client(user)
            elif choice == 2:
                navigate_client_search_menu(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_main_menus(user)


def navigate_client_search_menu(user: User):
    display_search_client_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_client_search_by_name(user)
            elif choice == 2:
                handle_client_search_by_commercial(user)
            elif choice == 3:
                handle_client_list_all_clients(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_client_menu(user)


def navigate_client_options(user: User, client: Client):
    display_client_options(user)
    while True:
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_client(user, client.id)
            elif choice == 2:
                delete_client(client.id)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_client_menu(user)


def navigate_contract_menu(user: User):
    display_contract_management_menu(user)
    while True:
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                add_contract(user)
            elif choice == 2:
                navigate_contract_search_menu(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    navigate_main_menus(user)


def navigate_contract_search_menu(user: User):
    display_search_contract_menu(user)
    while True:
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_search_contract_by_client(user)
            elif choice == 2:
                handle_search_contract_by_commercial(user)
            elif choice == 3:
                handle_search_all_contracts(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_contract_menu(user)


def navigate_contract_options(user: User, client: Client):
    display_contract_options(user)
    while True:
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_client(client.id)
            elif choice == 2:
                delete_client(client.id)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_client_menu(user)


def navigate_event_menu(user: User):
    display_event_management_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                return
            elif choice == 1:
                add_event(user)
            elif choice == 2:
                event_search_controller(user)
            elif choice == 3:
                break
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    navigate_main_menus(user)


def navigate_event_search_menu(user: User):
    display_search_event_menu(user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_search_event_by_contract(user)
            elif choice == 2:
                handle_search_event_by_support_contact(user)
            elif choice == 3:
                handle_search_event_without_support_contact(user)
            elif choice == 4:
                handle_search_event_by_client(user)
            elif choice == 5:
                handle_search_all_events(user)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_event_menu(user)


def navigate_event_options(user: User, event: Event):
    display_event_options(user)
    while True:
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_event(event.id)
            elif choice == 2:
                delete_event(event.id)
            else:
                print("Choix invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    navigate_event_menu(user)


def main_menu(user):
    navigate_main_menus(user)  # Remplacer l'appel direct à display_main_menu par navigate_menus
