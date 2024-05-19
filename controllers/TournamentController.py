from views.menu import MenuView
from models.Tournament import Tournament


class TournamentController:
    """Controls the tournament-related operations."""

    @staticmethod
    def create_tournament():
        """Create a new tournament."""
        name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        location = MenuView.get_user_input("Entrez le lieu du tournoi : ")
        start_date = MenuView.get_user_input("Entrez la date de début du tournoi (YYYY-MM-DD) : ")
        end_date = MenuView.get_user_input("Entrez la date de fin du tournoi (YYYY-MM-DD) : ")
        num_rounds = int(MenuView.get_user_input("Entrez le nombre de rounds du tournoi : "))
        tournament = Tournament(name, location, start_date, end_date, num_rounds, description="")
        TournamentController.save_tournament(tournament, f"./data/tournaments.json")
        if tournament:
            MenuView.display_message("Le tournoi a été créé avec succès !")
        else:
            MenuView.display_message("Une erreur s'est produite lors de la création du tournoi.")

    @staticmethod
    def display_tournaments():
        """Display the list of tournaments."""
        tournaments = TournamentController.get_all_tournaments()
        if tournaments:
            MenuView.display_message("Liste des tournois :")
            for tournament in tournaments:
                MenuView.display_message(f"{tournament.name} ({tournament.start_date} - {tournament.end_date})")
        else:
            MenuView.display_message("Aucun tournoi trouvé.")

    @staticmethod
    def display_tournament_details():
        """Display the details of a specific tournament."""
        tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        details = TournamentController.get_tournament_details(tournament_name)
        if details:
            MenuView.display_message(details)
        else:
            MenuView.display_message("Le tournoi spécifié n'a pas été trouvé.")

    @staticmethod
    def save_tournament(tournament, file_path):
        """
        Save the tournament data to a JSON file.

        Args:
            tournament (Tournament): The tournament instance to save.
            file_path (str): The path to the JSON file.
        """
        tournament.save_to_json(file_path)

    @staticmethod
    def load_tournament(tournament_name, file_path):
        """
        Load tournament data from a JSON file.

        Args:
            tournament_name(str): The name of the tournament.
            file_path (str): The path to the JSON file.

        Returns:
            Tournament: A Tournament instance loaded from the JSON data.
        """
        return Tournament.load_tournament(tournament_name, file_path)

    @staticmethod
    def get_all_tournaments():
        """
        Get a list of all tournaments.

        Returns:
            list: A list of Tournament instances.
        """
        file_path = "./data/tournaments.json"
        all_tournaments = Tournament.get_all_tournaments(file_path)
        return all_tournaments

    @staticmethod
    def get_tournament_details(tournament_name):
        """Get the name and dates of a specific tournament."""
        file_path = "./data/tournaments.json"
        tournaments = Tournament.get_all_tournaments(file_path)
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return (f"Tournament: {tournament.name}\nStart Date: {tournament.start_date}\nEnd Date:"
                        f" {tournament.end_date}")
        return "Aucun tournoi trouvé."
