class MenuView:
    """Class for displaying menu messages."""

    @staticmethod
    def display_main_menu():
        """Display the main menu options."""
        print("\nMenu Principal:")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Quitter le programme")

    @staticmethod
    def display_manage_players_menu():
        """Display the menu options for managing players."""
        print("\nMenu Gérer les Joueurs:")
        print("1. Ajouter un joueur")
        print("2. Afficher la liste des joueurs")
        print("3. Retourner au menu principal")

    @staticmethod
    def display_manage_tournaments_menu():
        """Display the menu options for managing tournaments."""
        print("\nMenu Gérer les Tournois:")
        print("1. Créer un nouveau tournoi")
        print("2. Afficher la liste des tournois")
        print("3. Afficher les détails d'un tournoi spécifique")
        print("4. Jouer un tournoi")
        print("5. Retourner au menu principal")

    @staticmethod
    def display_message(message):
        """Display a generic message."""
        print(message)

    @staticmethod
    def get_user_input(prompt):
        """Get user input."""
        return input(prompt)
