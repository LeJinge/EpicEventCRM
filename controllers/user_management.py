import typer
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.models import User, UserRole
from utils.db import SessionLocal
from passlib.context import CryptContext
from typing import List, Optional

from utils.validation import validate_user_data
from views.forms import user_form
from views.menus import display_search_collaborator_menu, display_collaborator_management_menu
from views.reports import display_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def handle_collaborator_management_menu():
    while True:
        typer.clear()
        display_collaborator_management_menu()
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent: ", type=int)

        if choice == 1:
            handle_add_user()
            typer.pause('Appuyez sur une touche pour continuer...')
        elif choice == 2:
            # Logique pour rechercher un collaborateur
            handle_collaborator_search_menu()
        elif choice == 0:
            break
        else:
            typer.echo("Choix invalide.")


# Gère l'ajout d'un nouvel utilisateur
def handle_add_user():
    user_data = user_form()
    try:
        # Assurez-vous que validate_user_data accepte 'role_str' comme argument
        validate_user_data(**user_data)

        # Conversion de 'role_str' en 'UserRole' après validation
        user_data['role'] = UserRole[user_data['role_str'].upper()]

        # 'role_str' n'est plus nécessaire après cette étape
        del user_data['role_str']

        # Création de l'utilisateur
        created_user = create_user(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            role=user_data['role'],
            password=user_data['password']
        )
        typer.echo(f"Utilisateur {created_user.first_name} {created_user.last_name} créé avec succès.")
    except ValueError as e:
        typer.echo(f"Erreur: {e}")


def create_user(first_name: str, last_name: str, email: str, role: UserRole, password: str) -> User:
    db: Session = SessionLocal()
    hashed_password = pwd_context.hash(password)
    user = User(first_name=first_name, last_name=last_name, email=email, role=role, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


# Gère la récupération des utilisateurs

def handle_collaborator_search_menu():
    db: Session = SessionLocal()
    users = db.query(User).all()  # Récupération initiale de tous les utilisateurs
    db.close()

    display_search_collaborator_menu()  # Affiche les options de menu
    choice = typer.prompt("Entrez votre choix (1-3): ", type=int)

    if choice == 1:
        name = typer.prompt("Entrez le nom du collaborateur à rechercher : ").lower()
        filtered_users = [user for user in users if name in user.first_name.lower() or name in user.last_name.lower()]
    elif choice == 2:
        role_str = typer.prompt("Entrez le rôle à rechercher (ex: Gestion, Commerciale, Support) : ")
        try:
            role = UserRole[role_str.upper()]
            filtered_users = [user for user in users if user.role == role]
        except KeyError:
            typer.echo(f"Erreur: Le rôle '{role_str}' n'est pas reconnu.")
            return
    elif choice == 3:
        filtered_users = users  # Aucun filtre appliqué, donc tous les utilisateurs sont sélectionnés
    else:
        typer.echo("Choix invalide.")
        return

    # Utilisez votre fonction d'affichage pour montrer les utilisateurs filtrés
    display_users(filtered_users)

    if filtered_users:
        user_choice = typer.prompt("Entrez le numéro du collaborateur pour voir plus d'options, ou 0 pour revenir : ",
                                   type=int)

        if user_choice == 0:
            return
        elif 0 < user_choice <= len(filtered_users):
            selected_user = filtered_users[user_choice - 1]
            handle_user_options(selected_user)
        else:
            typer.echo("Choix invalide.")
    else:
        typer.echo("Aucun utilisateur trouvé.")


def handle_user_options(user: User):
    while True:
        typer.echo(f"Sélectionné : {user.first_name} {user.last_name}")
        choice = typer.prompt("1. Modifier cet utilisateur\n2. Supprimer cet utilisateur\n0. Revenir", type=int)

        if choice == 1:
            first_name = typer.prompt("Nouveau prénom (laisser vide pour ne pas modifier) : ", default=user.first_name)
            last_name = typer.prompt("Nouveau nom (laisser vide pour ne pas modifier) : ", default=user.last_name)
            email = typer.prompt("Nouvel email (laisser vide pour ne pas modifier) : ", default=user.email)
            role = typer.prompt("Nouveau rôle (laisser vide pour ne pas modifier) : ", default=user.role.value)
            # Mettez à jour l'utilisateur avec les nouvelles valeurs
            update_user(user.id, first_name=first_name, last_name=last_name, email=email, role=role)
            typer.echo(f"L'utilisateur {first_name} {last_name} a été mis à jour.")
            break

        elif choice == 2:
            # Logique pour supprimer l'utilisateur
            if typer.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?"):
                delete_user(user.id)
                typer.echo(f"L'utilisateur {user.first_name} {user.last_name} a été supprimé.")
                break  # Sortir après suppression
        elif choice == 0:
            break  # Retour
        else:
            typer.echo("Choix invalide.")


# Gère la mise à jour d'un utilisateur
def update_user(user_id: int, first_name: str = None, last_name: str = None, email: str = None, role=None):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if role is not None:
            user.role = role
        db.commit()
        db.refresh(user)
    db.close()



# Gère la suppression d'un utilisateur
def delete_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
