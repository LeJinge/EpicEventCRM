import sentry_sdk
import typer
from passlib.context import CryptContext

from models.models import UserRole, User
from utils.db import SessionLocal
from utils.pagination import paginate_items
from utils.permissions import is_superuser, is_gestion
from views.forms import user_form, user_update_form
from views.messages import action_not_authorised, user_not_found, invalid_choice_try_again, update_user_success, \
    delete_user_success
from views.reports import display_user_profile, display_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Gère l'ajout d'un nouvel utilisateur
def add_user(connected_user: User):
    if is_superuser(connected_user) or is_gestion(connected_user):
        user_data = user_form()  # Assurez-vous que cette fonction valide bien les données entrées
        try:
            with SessionLocal() as db:
                user_role = UserRole[user_data['role_str'].upper()]
                hashed_password = pwd_context.hash(user_data['password'])
                new_user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    role=user_role,
                    password=hashed_password
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                typer.echo(f"Utilisateur {new_user.first_name} {new_user.last_name} créé avec succès.")
                return
        except KeyError:
            sentry_sdk.capture_exception()
            invalid_choice_try_again()
        except Exception as e:
            sentry_sdk.capture_exception()
            db.rollback()
            typer.echo(f"Erreur lors de la création de l'utilisateur: {str(e)}")
    else:
        action_not_authorised()


# Affichage et sélection d'un utilisateur spécifique
def display_and_select_user(connected_user: User, filtered_users):
    from controllers.menu_controller import navigate_user_options  # Assurez-vous que cette fonction existe

    if not filtered_users:
        user_not_found()
        return

    selected_user_id = paginate_items(filtered_users, display_users, 10)
    if selected_user_id is None:
        return  # Sortie anticipée si 'q' est pressé

    with SessionLocal() as db:
        selected_user = db.query(User).get(selected_user_id)
        if selected_user:
            typer.clear()
            display_user_profile(selected_user)
            navigate_user_options(connected_user, selected_user)


# Gère la recherche d'utilisateurs par nom
def handle_user_search_by_name(connected_user: User):
    db = SessionLocal()
    while True:  # Ajout d'une boucle pour permettre plusieurs tentatives
        try:
            last_name = typer.prompt("Entrez le nom de famille de l'utilisateur à rechercher (q pour sortir) ").lower()
            if last_name == "q":  # Permettre à l'utilisateur de sortir de la recherche
                return  # Retour simple pour quitter la fonction
            filtered_users = db.query(User).filter(User.last_name.ilike(f"%{last_name}%")).all()

            if not filtered_users:  # Si aucun utilisateur n'est trouvé
                user_not_found()
                continue  # Revenir au prompt initial

            display_and_select_user(connected_user, filtered_users)
            break  # Sortir après une sélection ou retourner au menu principal
        except Exception as e:
            sentry_sdk.capture_exception()
            typer.echo(f"Erreur lors de la recherche des utilisateurs: {e}")
        finally:
            db.close()  # Assurer la fermeture de la session DB


# Gère la recherche d'utilisateurs par rôle
def handle_user_search_by_role(connected_user: User):
    with SessionLocal() as db:
        role_str = typer.prompt("Entrez le rôle à rechercher (ex: Admin, User): ").upper()
        try:
            role = UserRole[role_str]
            filtered_users = db.query(User).filter(User.role == role).all()
            display_and_select_user(connected_user, filtered_users)
        except KeyError:
            sentry_sdk.capture_exception()
            typer.echo(f"Rôle '{role_str}' non reconnu.")


def handle_list_all_users(connected_user: User):
    db = SessionLocal()
    try:
        filtered_users = db.query(User).all()
        display_and_select_user(connected_user, filtered_users)
    finally:
        db.close()


# Gère la mise à jour d'un utilisateur
def update_user(connected_user: User, user_id: int):
    from controllers.menu_controller import navigate_user_menu
    if is_superuser(connected_user) or is_gestion(connected_user):
        db = SessionLocal()
        try:
            user = db.query(User).get(user_id)
            if not user:
                user_not_found()
                return

            update_data = user_update_form(user)  # Assurez-vous que cette fonction est définie

            # Mise à jour des informations de l'utilisateur
            user.first_name = update_data.get("first_name", user.first_name)
            user.last_name = update_data.get("last_name", user.last_name)
            user.email = update_data.get("email", user.email)
            user.role = UserRole[update_data.get("role_str", user.role.name).upper()]
            # Assurez-vous de gérer correctement les changements de mot de passe ou d'autres champs sensibles

            db.commit()
            update_user_success()
            display_user_profile(user)
            typer.pause('Appuyez sur Entrée pour continuer...')
            navigate_user_menu(connected_user)
        except Exception as e:
            sentry_sdk.capture_exception()
            db.rollback()
            typer.echo(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
        finally:
            db.close()
    else:
        action_not_authorised()


# Gère la suppression d'un utilisateur
def delete_user(connected_user: User, user_id: int):
    from controllers.menu_controller import navigate_user_menu
    if not is_superuser(connected_user):
        action_not_authorised()
        return

    db = SessionLocal()
    try:
        user = db.query(User).get(user_id)
        if user:
            db.delete(user)
            db.commit()
            delete_user_success()
        else:
            user_not_found()
    finally:
        db.close()
        return navigate_user_menu(connected_user)

# Gère la mise à jour d'un utilisateur
