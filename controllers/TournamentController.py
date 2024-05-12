from models.Tournament import Tournament
import os
import json


class TournamentController:
    """Controls the tournament-related operations."""

    @staticmethod
    def create_tournament(name, location, start_date, end_date, num_rounds=4, current_round=1, description=""):
        """Create a new tournament."""
        tournament = Tournament(name, location, start_date, end_date, num_rounds, current_round, description)
        TournamentController.save_tournament(tournament, f"./data/tournaments.json")
        return tournament

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
        tournaments = Tournament.get_all_tournaments(file_path)  # On utilise la méthode statique de la classe Tournament
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return (f"Tournament: {tournament.name}\nStart Date: {tournament.start_date}\nEnd Date:"
                        f" {tournament.end_date}")
        return "Aucun tournoi trouvé."
