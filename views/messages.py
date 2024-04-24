import typer


def invalid_choice_try_again():
    typer.echo("Choix invalide, veuillez réessayer.")


def event_not_found():
    typer.echo("Aucun événement trouvé.")


def action_not_authorised():
    typer.echo("Action non autorisée.")


def user_not_found():
    typer.echo("Utilisateur non trouvé.")


def contract_not_found():
    typer.echo("Aucun contrat trouvé.")


def number_not_valid():
    typer.echo("Veuillez entrer un nombre valide.")


def successful_logout():
    typer.echo("Déconnexion réussie.")


def client_not_found():
    typer.echo("Aucun client trouvé.")


def commercial_not_found():
    typer.echo("Aucun commercial trouvé.")


def add_contract_success():
    typer.echo("Contrat ajouté avec succès.")


def add_event_success():
    typer.echo("Événement ajouté avec succès.")


def update_event_success():
    typer.echo("Événement mis à jour avec succès.")


def delete_contract_success():
    typer.echo("Contrat supprimé avec succès.")


def update_contract_success():
    typer.echo("Contrat mis à jour avec succès.")


def update_user_success():
    typer.echo("Utilisateur mis à jour avec succès.")


def delete_event_success():
    typer.echo("Événement supprimé avec succès.")


def delete_user_success():
    typer.echo("Utilisateur supprimé avec succès.")


def update_client_success():
    typer.echo("Client mis à jour avec succès.")


def delete_client_success():
    typer.echo("Client supprimé avec succès.")
