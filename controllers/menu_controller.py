import sentry_sdk
import typer

from controllers.client_management import add_client, update_client, delete_client, \
    handle_client_search_by_name, handle_client_search_by_commercial, handle_client_list_all_clients
from controllers.contract_management import add_contract, handle_search_contract_by_client, \
    handle_search_contract_by_commercial, handle_search_all_contracts, update_contract, delete_contract, \
    handle_search_contracts_in_progress, handle_search_contracts_not_fully_paid
from controllers.event_management import add_event, update_event, \
    handle_search_event_by_contract, handle_search_event_by_support_contact, \
    handle_search_event_without_support_contact, handle_search_event_by_client, handle_search_all_events, delete_event
from controllers.logout_controller import logout
from controllers.user_management import add_user, handle_user_search_by_role, handle_list_all_users, \
    update_user, delete_user, handle_user_search_by_name
from models.models import User, Client, Event, Contract
from utils.permissions import is_superuser, is_gestion, is_commerciale, is_support
from views.menu import display_main_menu, display_contract_management_menu, display_event_management_menu, \
    display_client_management_menu, display_search_user_menu, display_user_management_menu, display_user_options, \
    display_search_client_menu, display_client_options, display_search_menu, display_search_contract_menu, \
    display_contract_options, display_event_options, display_search_event_menu
from views.messages import invalid_choice_try_again, action_not_authorised, number_not_valid


def navigate_main_menus(connected_user: User):
    while True:
        try:
            typer.clear()
            display_main_menu(connected_user)
            choice = int(typer.prompt("Entrez votre choix ou 0 pour quitter "))
        except ValueError:
            sentry_sdk.capture_exception()
            invalid_choice_try_again()
            return

        if choice == 0:
            logout()
            break
        elif choice == 1:
            navigate_search_menu(connected_user)
        else:
            if is_superuser(connected_user):
                if choice == 2:
                    navigate_user_menu(connected_user)
                elif choice == 3:
                    navigate_client_menu(connected_user)
                elif choice == 4:
                    navigate_contract_menu(connected_user)
                elif choice == 5:
                    navigate_event_menu(connected_user)
            elif is_gestion(connected_user):
                if choice == 2:
                    navigate_user_menu(connected_user)
                elif choice == 3:
                    navigate_contract_menu(connected_user)
                elif choice == 4:
                    navigate_event_menu(connected_user)
            elif is_commerciale(connected_user):
                if choice == 2:
                    navigate_client_menu(connected_user)
                elif choice == 3:
                    navigate_contract_menu(connected_user)
                elif choice == 4:
                    navigate_event_menu(connected_user)
            elif is_support(connected_user):
                if choice == 2:
                    navigate_event_menu(connected_user)
            else:
                invalid_choice_try_again()
                return navigate_main_menus(connected_user)


def navigate_user_menu(connected_user: User):
    if is_superuser(connected_user) or is_gestion(connected_user):
        while True:
            typer.clear()
            display_user_management_menu(connected_user)
            try:
                choice = int(typer.prompt(
                    "Entrez votre choix (Entrez votre choix ou 0 pour quitter) "))
                if choice == 0:
                    break
                elif choice == 1:
                    add_user(connected_user)
                elif choice == 2:
                    navigate_user_search_menu(connected_user)
                else:
                    invalid_choice_try_again()
            except ValueError:
                sentry_sdk.capture_exception()
                invalid_choice_try_again()
        return

    else:
        action_not_authorised()
        return


def navigate_user_search_menu(connected_user: User):
    while True:
        typer.clear()
        display_search_user_menu(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_user_search_by_name(connected_user)
            elif choice == 2:
                handle_user_search_by_role(connected_user)
            elif choice == 3:
                handle_list_all_users(connected_user)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            invalid_choice_try_again()
    return


def navigate_user_options(connected_user: User, selected_user: User):
    while True:
        display_user_options(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_user(connected_user, selected_user.id)
            elif choice == 2:
                delete_user(connected_user, selected_user.id)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            invalid_choice_try_again()
    return


def navigate_search_menu(connected_user: User):
    while True:
        display_search_menu()
        try:
            choice = typer.prompt("Entrez votre choix (1-4): ", type=int)

            if choice == 1:
                navigate_user_search_menu(connected_user),
            elif choice == 2:
                navigate_client_search_menu(connected_user),
            elif choice == 3:
                navigate_contract_menu(connected_user),
            elif choice == 4:
                navigate_event_menu(connected_user),
            elif choice == 0:
                break
            else:  # Choix invalide
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            invalid_choice_try_again()


def navigate_client_menu(connected_user: User):
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        typer.clear()
        display_client_management_menu(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                add_client(connected_user)
            elif choice == 2:
                navigate_client_search_menu(connected_user)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()
    navigate_main_menus(connected_user)


def navigate_client_search_menu(connected_user: User):
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        typer.clear()
        display_search_client_menu(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter navigate_client_search_menu): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_client_search_by_name(connected_user)
            elif choice == 2:
                handle_client_search_by_commercial(connected_user)
            elif choice == 3:
                handle_client_list_all_clients(connected_user)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()


def navigate_client_options(connected_user: User, client: Client):
    while True:
        display_client_options(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                navigate_client_menu(connected_user)
            elif choice == 1:
                update_client(connected_user, client.id)
            elif choice == 2:
                delete_client(connected_user, client.id)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()


def navigate_contract_menu(connected_user: User):
    typer.clear()
    while True:
        display_contract_management_menu(connected_user)
        if is_superuser(connected_user) or is_gestion(connected_user):
            try:
                choice = int(input(
                    "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
                if choice == 0:
                    break
                elif choice == 1:
                    add_contract(connected_user)
                elif choice == 2:
                    navigate_contract_search_menu(connected_user)
                else:
                    invalid_choice_try_again()
            except ValueError:
                sentry_sdk.capture_exception()
                number_not_valid()
        elif is_commerciale(connected_user):
            try:
                choice = int(input(
                    "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
                if choice == 0:
                    break
                elif choice == 1:
                    navigate_contract_search_menu(connected_user)
                else:
                    invalid_choice_try_again()
            except ValueError:
                sentry_sdk.capture_exception()
                number_not_valid()
        else:
            action_not_authorised()
            return

        navigate_main_menus(connected_user)


def navigate_contract_search_menu(connected_user: User):
    typer.clear()
    while True:
        display_search_contract_menu(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_search_contract_by_client(connected_user)
            elif choice == 2:
                handle_search_contract_by_commercial(connected_user)
            elif choice == 3:
                handle_search_contracts_in_progress(connected_user)
            elif choice == 4:
                handle_search_contracts_not_fully_paid(connected_user)
            elif choice == 5:
                handle_search_all_contracts(connected_user)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()
    navigate_contract_menu(connected_user)


def navigate_contract_options(connected_user: User, contract: Contract):
    while True:
        display_contract_options(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_contract(connected_user, contract.id)
            elif choice == 2:
                delete_contract(connected_user, contract.id)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()
    navigate_contract_menu(connected_user)


def navigate_event_menu(connected_user: User):
    display_event_management_menu(connected_user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        if is_superuser(connected_user) or is_commerciale(connected_user):
            try:
                choice = int(input(
                    "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
                if choice == 1:
                    add_event(connected_user)
                elif choice == 2:
                    navigate_event_search_menu(connected_user)
                elif choice == 0:
                    break
                else:
                    invalid_choice_try_again()
                    continue
            except ValueError:
                sentry_sdk.capture_exception()
                number_not_valid()
        elif is_gestion(connected_user) or is_support(connected_user):
            try:
                choice = int(input(
                    "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
                if choice == 1:
                    navigate_event_search_menu(connected_user)
                elif choice == 0:
                    break
                else:
                    invalid_choice_try_again()
                    continue
            except ValueError:
                sentry_sdk.capture_exception()
                number_not_valid()
        else:
            action_not_authorised()
        navigate_main_menus(connected_user)


def navigate_event_search_menu(connected_user: User):
    display_search_event_menu(connected_user)
    while True:  # Boucle jusqu'à ce que l'utilisateur choisisse de sortir
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                handle_search_event_by_contract(connected_user)
            elif choice == 2:
                handle_search_event_by_support_contact(connected_user)
            elif choice == 3:
                handle_search_event_without_support_contact(connected_user)
            elif choice == 4:
                handle_search_event_by_client(connected_user)
            elif choice == 5:
                handle_search_all_events(connected_user)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()
    navigate_event_menu(connected_user)


def navigate_event_options(connected_user: User, event: Event):
    while True:
        display_event_options(connected_user)
        try:
            choice = int(input(
                "Entrez votre choix (Entrez votre choix ou 0 pour quitter): "))
            if choice == 0:
                break
            elif choice == 1:
                update_event(connected_user, event.id)
            elif choice == 2:
                delete_event(connected_user, event.id)
            else:
                invalid_choice_try_again()
        except ValueError:
            sentry_sdk.capture_exception()
            number_not_valid()
    navigate_event_menu(connected_user)


def main_menu(connected_user: User):
    navigate_main_menus(connected_user)  # Remplacer l'appel direct à display_main_menu par navigate_menus
