import typer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.models import User, UserRole
from utils.db import SessionLocal
from utils.pagination import paginate_items
from views.forms import user_form, user_update_form
from views.menus import display_collaborator_management_menu, display_search_user_menu, display_user_options
from views.reports import display_user_profile, display_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def handle_collaborator_management_menu():
    while True:
        typer.clear()
        display_collaborator_management_menu()
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent ", type=int)

        if choice == 1:
            add_user()
            typer.pause('Appuyez sur une touche pour continuer...')
        elif choice == 2:
            # Logique pour rechercher un collaborateur
            user_search_controller()
        elif choice == 0:
            break
        else:
            typer.echo("Choix invalide.")


# Gère l'ajout d'un nouvel utilisateur
def add_user():
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
    except KeyError as e:
        typer.echo(f"Erreur: Rôle non valide.")
    except Exception as e:
        typer.echo(f"Erreur lors de la création de l'utilisateur: {e}")


# Gère la récupération des utilisateurs


def user_search_controller():
    typer.clear()
    display_search_user_menu()
    choice = typer.prompt("Entrez votre choix (1-3): ", type=int)

    with SessionLocal() as db:
        if choice == 1:  # Recherche par nom
            last_name = typer.prompt("Entrez le nom de famille de l'utilisateur à rechercher: ").lower()
            filtered_users = db.query(User).filter(User.last_name.ilike(f"%{last_name}%")).all()
        elif choice == 2:  # Recherche par rôle
            role_str = typer.prompt("Entrez le rôle à rechercher (ex: Admin, User): ").upper()
            try:
                role = UserRole[role_str]
                filtered_users = db.query(User).filter(User.role == role).all()
            except KeyError:
                typer.echo(f"Rôle '{role_str}' non reconnu.")
                return
        elif choice == 3:  # Afficher tous les utilisateurs
            filtered_users = db.query(User).all()
        else:
            typer.echo("Choix invalide.")
            return

        if filtered_users:
            selected_user_id = paginate_items(filtered_users, display_users)
            if selected_user_id is not None:
                selected_user = db.query(User).get(selected_user_id)
                if selected_user:
                    display_user_profile(selected_user)
                    action_choice = display_user_options(selected_user)
                    if action_choice == 1:
                        update_user(selected_user.id)
                    elif action_choice == 2:
                        if typer.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?"):
                            delete_user(selected_user.id)
                            typer.echo(
                                f"L'utilisateur {selected_user.first_name} {selected_user.last_name} a été supprimé.")
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
def delete_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
