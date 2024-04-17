from typing import List, Callable, Any, Optional
from rich.console import Console
from rich.table import Table


def paginate_items(items: List[Any], display_function: Callable[[List, int], Table], per_page: int = 10):
    console = Console()
    total_pages = max(1, (len(items) + per_page - 1) // per_page)

    page = 1
    while True:
        console.clear()
        start_index = (page - 1) * per_page
        page_items = items[start_index:start_index + per_page]

        table = display_function(page_items, start_index + 1)
        console.print(table)

        console.print(
            f"Page {page}/{total_pages}. 'n' pour suivant, 'p' pour précédent, 'q' pour quitter, ou sélectionnez un ID ou laissez vide pour ne rien changer.")
        user_input = console.input("Choix : ").strip().lower()

        if user_input == "":
            return None  # L'utilisateur choisit de ne rien changer
        elif user_input.isdigit() and 0 < int(user_input) <= len(items):
            selected_index = int(user_input) - 1
            return items[selected_index].id
        elif user_input == 'n' and page < total_pages:
            page += 1
        elif user_input == 'p' and page > 1:
            page -= 1
        elif user_input == 'q':
            return None
        else:
            console.print("Commande inconnue.", style="bold red")
