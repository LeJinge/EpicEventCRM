import typer

from views.menus import display_client_management_menu


def handle_client_management_menu():
    while True:
        typer.clear()
        display_client_management_menu()
        choice = typer.prompt("Entrez votre choix (1-2) ou 0 pour revenir au menu précédent: ", type=int)

        if choice == 1:
            # Ajouter un client
            pass
        elif choice == 2:
            # Rechercher un client
            pass
        elif choice == 0:
            break
        else:
            typer.echo("Choix invalide.")


def handle_add_user():
    client_data = client_form()
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