from typing import List

import typer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.models import User, UserRole
from utils.db import SessionLocal
from utils.validation import validate_user_data
from views.forms import user_form, user_update_form
from views.menus import display_search_collaborator_menu, display_collaborator_management_menu
from views.reports import display_users, display_user_profile

from rich.console import Console
from rich.table import Table

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def handle_collaborator_management_menu():
    while True:
        typer.clear()
        display_collaborator_management_menu()
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent ", type=int)

        if choice == 1:
            handle_add_user()
            typer.pause('Appuyez sur une touche pour continuer...')
        elif choice == 2:
            # Logique pour rechercher un collaborateur
            collaborator_search_menu_controller()
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

def get_users() -> List[User]:
    db: Session = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


def collaborator_search_menu_controller():
    typer.clear()
    display_search_collaborator_menu()
    choice = typer.prompt("Entrez votre choix (1-3): ", type=int)
    users = get_users()

    if choice == 1:
        search_by_name(users)
    elif choice == 2:
        search_by_team(users)
    elif choice == 3:
        display_all_collaborators(users)
    else:
        typer.echo("Choix invalide.")


def user_options(user: User):
    choice = typer.prompt(
        "Choisissez une option : \n1. Modifier cet utilisateur\n2. Supprimer cet utilisateur\n0. Retour", type=int)

    if choice == 1:
        update_user(user.id)  # Implémentez cette fonction selon vos besoins
    elif choice == 2:
        if typer.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?"):
            delete_user(user.id)  # Assurez-vous que cette fonction est implémentée correctement
            typer.echo(f"L'utilisateur {user.first_name} {user.last_name} a été supprimé.")
    elif choice == 0:
        return
    else:
        typer.echo("Choix invalide.")


def paginate_users(users: List[User], page: int = 1, per_page: int = 10):
    console = Console()
    total_pages = len(users) // per_page + (1 if len(users) % per_page else 0)
    start = (page - 1) * per_page
    end = start + per_page
    page_users = users[start:end]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Numéro", style="dim", width=6)
    table.add_column("Prénom", min_width=20)
    table.add_column("Nom", min_width=20)
    table.add_column("Rôle", min_width=20)

    for index, user in enumerate(page_users, start=start + 1):
        table.add_row(str(index), user.first_name, user.last_name, user.role.name)

    console.print(table)
    console.print(
        f"Page {page}/{total_pages}. 'n' pour suivant, 'p' pour précédent, 'q' pour quitter, numéro pour sélectionner.")

    while True:
        choice = console.input("Choix: ").strip()

        if choice.isdigit():
            user_choice = int(choice)
            if start < user_choice <= end:
                typer.clear()
                selected_user = users[user_choice - 1]
                display_user_profile(selected_user)
                user_options(selected_user)
            else:
                console.print("Choix invalide.", style="bold red")
        elif choice.lower() == 'n' and page < total_pages:
            return paginate_users(users, page + 1, per_page)
        elif choice.lower() == 'p' and page > 1:
            return paginate_users(users, page - 1, per_page)
        elif choice.lower() == 'q':
            break
        else:
            console.print("Commande inconnue.", style="bold red")


def search_by_name(users: List[User]):
    typer.clear()
    last_name = typer.prompt("Entrez le nom de famille du collaborateur à rechercher ").lower()
    filtered_users = [user for user in users if last_name == user.last_name.lower()]

    if filtered_users:
        if len(filtered_users) == 1:
            typer.clear()
            display_user_profile(filtered_users[0])
            user_options(filtered_users[0])
        else:
            typer.echo("Plusieurs utilisateurs trouvés avec ce nom de famille. Veuillez affiner votre recherche.")
            for index, user in enumerate(filtered_users, start=1):
                typer.echo(f"{index}. {user.first_name} {user.last_name}")
            user_index = typer.prompt("Sélectionnez le numéro de l'utilisateur : ", type=int) - 1
            if 0 <= user_index < len(filtered_users):
                display_user_profile(filtered_users[user_index])
            else:
                typer.echo("Sélection invalide.")
    else:
        typer.echo("Aucun utilisateur trouvé correspondant au nom de famille donné.")


def search_by_team(users: List[User]):
    role_str = typer.prompt("Entrez le rôle à rechercher (ex: Gestion, Commerciale, Support) ")
    try:
        role = UserRole[role_str.upper()]
        filtered_users = [user for user in users if user.role == role]
        if filtered_users:
            paginate_users(filtered_users)
        else:
            typer.echo("Aucun utilisateur trouvé pour ce rôle.")
    except KeyError:
        typer.echo(f"Erreur: Le rôle '{role_str}' n'est pas reconnu.")


def display_all_collaborators(users: List[User]):
    paginate_users(users)


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
