import typer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from typer import Typer

from models.models import UserRole, User
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.forms import user_form, user_update_form
from views.reports import display_user_profile, display_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = Typer()


# Gère l'ajout d'un nouvel utilisateur
def add_user(user: User):
    # Vérifier si l'utilisateur actuel a le droit d'ajouter un nouvel utilisateur
    if current_user.role not in [UserRole.SUPERUSER, UserRole.GESTION]:
        typer.echo(
            "Action non autorisée. Seuls les superutilisateurs et les gestionnaires peuvent ajouter des utilisateurs.")
        return
    user_data = user_form()  # Récupère les données du formulaire
    try:
        # Convertit le rôle de l'utilisateur de chaîne à Enum, après avoir validé les données
        user_role = UserRole[user_data['role_str'].upper()]

        # Hashage du mot de passe
        hashed_password = pwd_context.hash(user_data['password'])

        with SessionLocal() as db:
            # Crée l'instance de l'utilisateur
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                role=user_role,
                password=hashed_password
            )

            # Ajoute et commit l'utilisateur dans la base de données
            db.add(user)
            db.commit()
            db.refresh(user)

            typer.echo(f"Utilisateur {user.first_name} {user.last_name} créé avec succès.")
            return
    except KeyError as e:
        typer.echo(f"Erreur: Rôle non valide.")
    except Exception as e:
        typer.echo(f"Erreur lors de la création de l'utilisateur: {e}")


# Gère la récupération des utilisateurs


def handle_search_by_name(db: Session):
    last_name = typer.prompt("Entrez le nom de famille de l'utilisateur à rechercher: ").lower()
    filtered_users = db.query(User).filter(User.last_name.ilike(f"%{last_name}%")).all()
    display_and_select_user(filtered_users, db)


def handle_search_by_role(db: Session):
    role_str = typer.prompt("Entrez le rôle à rechercher (ex: Admin, User): ").upper()
    try:
        role = UserRole[role_str]
        filtered_users = db.query(User).filter(User.role == role).all()
        display_and_select_user(filtered_users, db)
    except KeyError:
        typer.echo(f"Rôle '{role_str}' non reconnu.")


def handle_list_all_users(db: Session):
    filtered_users = db.query(User).all()
    display_and_select_user(filtered_users, db)


def display_and_select_user(filtered_users, db):
    from controllers.menu_controller import navigate_user_options
    if filtered_users:
        selected_user_id = paginate_items(filtered_users, display_users, 10)
        if selected_user_id:
            selected_user = db.query(User).get(selected_user_id)
            display_user_profile(selected_user)
            navigate_user_options(selected_user)
    else:
        typer.echo("Aucun utilisateur trouvé.")


# Gère la mise à jour d'un utilisateur
def update_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo("Utilisateur non trouvé.")
        return

    first_name, last_name, email, role_str = user_update_form(user)

    try:
        role = UserRole[role_str.upper()]
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        db.commit()
        typer.echo("Utilisateur mis à jour avec succès.")
        db.refresh(user)  # S'assurer d'avoir les données les plus à jour
        typer.clear()
        display_user_profile(user)  # Afficher la fiche mise à jour
        typer.pause('Appuyez sur une touche pour revenir au menu "Gestion des collaborateurs"...')
    except Exception as e:
        db.rollback()
        typer.echo(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
    finally:
        db.close()


# Gère la suppression d'un utilisateur
def delete_user(user: User, user_id: int):
    # Vérifier si l'utilisateur actuel a le droit d'ajouter un nouvel utilisateur
    if user.role not in [UserRole.SUPERUSER]:
        print(
            "Action non autorisée. Seuls les superutilisateurs et les gestionnaires peuvent ajouter des utilisateurs.")
        return
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
