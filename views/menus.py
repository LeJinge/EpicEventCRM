from rich.console import Console


def display_management_main_menu():
    console = Console()
    options = [
        '1. Gérer les collaborateurs',
        '2. Gérer les clients',
        '3. Gérer les contrats',
        '4. Gérer les événements'
    ]
    console.print("[bold magenta]Menu Gestion[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_commercial_main_menu():
    console = Console()
    options = [
        '1. Gérer les clients',
        '2. Gérer les contrats',
        '3. Gérer les événements'
    ]
    console.print("[bold magenta]Menu Gestion[/bold magenta]\n")
    for option in options:
        console.print(option)

    # Cet input est juste pour la structure,
    # la vraie saisie utilisateur se fera dans le controller pour séparer les préoccupations.
    input_prompt = "Entrez votre choix (1-3): "
    console.print(input_prompt, end="", style="bold yellow")
    # Ne retourne pas la vraie entrée ici, mais affiche l'invite pour comprendre où elle sera.


def display_support_main_menu():
    console = Console()
    options = [
        '1. Gérer les événements'
    ]
    console.print("[bold magenta]Menu Gestion[/bold magenta]\n")
    for option in options:
        console.print(option)

    # Cet input est juste pour la structure,
    # la vraie saisie utilisateur se fera dans le controller pour séparer les préoccupations.
    input_prompt = "Entrez votre choix (1): "
    console.print(input_prompt, end="", style="bold yellow")
    # Ne retourne pas la vraie entrée ici, mais affiche l'invite pour comprendre où elle sera.


def display_collaborator_management_menu():
    console = Console()
    options = [
        "1. Ajouter un collaborateur",
        "2. Rechercher un collaborateur",
        "0. Retour au menu précédent",
    ]
    console.print("[bold magenta]Gestion des collaborateurs[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_search_collaborator_menu():
    console = Console()
    options = [
        "1. Rechercher par nom",
        "2. Rechercher par équipe",
        "3. Tous les collaborateurs",
    ]
    console.print("[bold magenta]Rechercher un collaborateur[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_client_management_menu():
    console = Console()
    options = [
        "1. Ajouter un client",
        "2. Rechercher un client",
    ]
    console.print("[bold magenta]Gestion des clients[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_search_client_menu():
    console = Console()
    options = [
        "1. Rechercher par nom",
        "2. Par commerciale",
        "3. Tous les clients",
        ]
    console.print("[bold magenta]Rechercher un client[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_contract_management_menu():
    console = Console()
    options = [
        "1. Ajouter un contrat",
        "2. Rechercher un contrat",
    ]
    console.print("[bold magenta]Gestion des contrats[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_search_contract_menu():
    console = Console()
    options = [
        "1. Rechercher par client",
        "2. Par commerciale",
        "3. Tous les contrats",
    ]
    console.print("[bold magenta]Rechercher un contrat[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_event_management_menu():
    console = Console()
    options = [
        "1. Ajouter un événement",
        "2. Rechercher un événement",
    ]
    console.print("[bold magenta]Gestion des événements[/bold magenta]\n")
    for option in options:
        console.print(option)


def display_search_event_menu():
    console = Console()
    options = [
        "1. Rechercher par client",
        "2. Par support",
        "3. Par contrat",
        "4. Tous les événements",
        ]
    console.print("[bold magenta]Rechercher un événement[/bold magenta]\n")
    for option in options:
        console.print(option)


