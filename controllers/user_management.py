import typer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.models import UserRole, User
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.forms import user_form, user_update_form
from views.reports import display_user_profile, display_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Gère l'ajout d'un nouvel utilisateur
def add_user(current_user: User):
    from controllers.menu_controller import navigate_user_menu
    if current_user.role not in [UserRole.SUPERUSER, UserRole.GESTION]:
        typer.echo(
            "Action non autorisée. Seuls les superutilisateurs et les gestionnaires peuvent ajouter des utilisateurs.")
        return

    user_data = user_form()
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
            navigate_user_menu(current_user)
    except KeyError:
        typer.echo("Erreur: Rôle non valide.")
    except Exception as e:
        typer.echo(f"Erreur lors de la création de l'utilisateur: {e}")


# Affichage et sélection d'un utilisateur spécifique
def display_and_select_user(current_user: User, filtered_users):
    from controllers.menu_controller import navigate_user_options
    with SessionLocal() as db:
        if filtered_users:
            selected_user_id = paginate_items(filtered_users, display_users, 10)
            if selected_user_id:
                selected_user = db.query(User).get(selected_user_id)
                typer.clear()
                display_user_profile(selected_user)
                navigate_user_options(current_user, selected_user)
        else:
            typer.echo("Aucun utilisateur trouvé.")


# Gère la recherche d'utilisateurs par nom
def handle_search_by_name(current_user: User):
    with SessionLocal() as db:
        last_name = typer.prompt("Entrez le nom de famille de l'utilisateur à rechercher: ").lower()
        filtered_users = db.query(User).filter(User.last_name.ilike(f"%{last_name}%")).all()
        display_and_select_user(current_user, filtered_users)


# Gère la recherche d'utilisateurs par rôle
def handle_search_by_role(current_user: User):
    with SessionLocal() as db:
        role_str = typer.prompt("Entrez le rôle à rechercher (ex: Admin, User): ").upper()
        try:
            role = UserRole[role_str]
            filtered_users = db.query(User).filter(User.role == role).all()
            display_and_select_user(current_user, filtered_users)
        except KeyError:
            typer.echo(f"Rôle '{role_str}' non reconnu.")


def handle_list_all_users(user: User):
    db = SessionLocal()
    try:
        filtered_users = db.query(User).all()
        display_and_select_user(user, filtered_users, db)
    finally:
        db.close()


# Gère la mise à jour d'un utilisateur
def update_user(user: User):
    from controllers.menu_controller import navigate_user_menu
    with SessionLocal() as db:
        existing_user = db.query(User).get(user.id)
        if not existing_user:
            typer.echo("Utilisateur non trouvé.")
            return

        update_data = user_update_form(existing_user)
        existing_user.first_name = update_data['first_name']
        existing_user.last_name = update_data['last_name']
        existing_user.email = update_data['email']
        existing_user.role = UserRole[update_data['role_str'].upper()]
        db.commit()
        typer.clear()
        display_user_profile(existing_user)
        typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des utilisateurs"...')
        navigate_user_menu(user)


# Gère la suppression d'un utilisateur
def delete_user(current_user: User):
    if current_user.role not in [UserRole.SUPERUSER]:
        typer.echo("Action non autorisée. Seuls les superutilisateurs peuvent supprimer des utilisateurs.")
        return

    with SessionLocal() as db:
        target_user = db.query(User).filter(User.id).first()
        if target_user:
            db.delete(target_user)
            db.commit()
            typer.echo("Utilisateur supprimé avec succès.")
        else:
            typer.echo("Utilisateur non trouvé.")

# Gère la mise à jour d'un utilisateur
