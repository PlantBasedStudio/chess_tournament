import json
import os
from models.Match import Match
from models.Player import Player
from models.Round import Round


class Tournament:
    """Represents a chess tournament."""

    def __init__(self, name, location, start_date, end_date, num_rounds=4, current_round=1, description=""):
        """
        Initialize a tournament.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in the format 'YYYY-MM-DD'.
            end_date (str): The end date of the tournament in the format 'YYYY-MM-DD'.
            num_rounds (int): The number of rounds in the tournament (default is 4).
            current_round (int): The number of the current round (default is 1).
            description (str): General remarks about the tournament (default is "").
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.current_round = current_round
        self.description = description
        self.rounds = [[] for _ in range(num_rounds)]
        self.registered_players = []

    def generate_rounds(self, players):
        """Generate rounds with matches based on player standings."""
        # Logic to sort players and generate match pairs for each round
        for round_number in range(self.num_rounds):
            round_name = f"Round {round_number + 1}"
            round_instance = Round(round_name)
            # Generate matches for the round
            matches = round_instance.generate_matches(players)
            # Add matches to the round
            round_instance.add_matches(matches)
            # Add the round with matches to the tournament
            self.rounds[round_number].append(round_instance)

    def add_player(self, player):
        """
        Add a player to the tournament.

        Args:
            player (Player): The player to be added to the tournament.
        """
        self.registered_players.append(player)

    def save_to_json(self, file_path):
        """
        Save the tournament data to a JSON file.

        Args:
            file_path (str): The path to the JSON file.
        """
        data_dir = './data'
        # Créez le dossier data/tournaments s'il n'existe pas
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        tournament_data = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "description": self.description,
            "registered_players": [player.__dict__ for player in self.registered_players],
            "rounds": [[match.__dict__ for match in round_matches] for round_matches in self.rounds]
        }

        # Load existing tournament data from the JSON file
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                all_tournaments = json.load(json_file)
        else:
            all_tournaments = []

        # Append the new tournament data to the list
        all_tournaments.append(tournament_data)

        # Save the updated tournament data back to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(all_tournaments, json_file, indent=4)

    @staticmethod
    def load_tournament(tournament_name, file_path):
        """
        Load tournament data from a JSON file.

        Args:
            tournament_name (str): The name of the tournament.
            file_path (str): The path to the JSON file.

        Returns:
            Tournament: A Tournament instance loaded from the JSON data.
        """
        try:
            with open(file_path, 'r') as json_file:
                all_tournaments_data = json.load(json_file)
        except FileNotFoundError:
            return None

        for tournament_data in all_tournaments_data:
            if tournament_data['name'] == tournament_name:
                tournament = Tournament(
                    tournament_data['name'],
                    tournament_data['location'],
                    tournament_data['start_date'],
                    tournament_data['end_date'],
                    tournament_data['num_rounds'],
                    tournament_data['current_round'],
                    tournament_data['description']
                )
                tournament.registered_players = tournament_data['registered_players']
                tournament.rounds = tournament_data['rounds']
                return tournament

        return None

    @classmethod
    def get_all_tournaments(cls, file_path):
        """
        Get a list of all tournaments.

        Args:
            file_path (str): The path to the JSON file containing tournament data.

        Returns:
            list: A list of Tournament instances.
        """
        try:
            with open(file_path, 'r') as json_file:
                all_tournaments_data = json.load(json_file)
        except FileNotFoundError:
            return []

        all_tournaments = []
        for tournament_data in all_tournaments_data:
            tournament = cls(
                tournament_data['name'],
                tournament_data['location'],
                tournament_data['start_date'],
                tournament_data['end_date'],
                tournament_data['num_rounds'],
                tournament_data['current_round'],
                tournament_data['description']
            )
            tournament.registered_players = [Player(**player_data) for player_data in
                                             tournament_data['registered_players']]
            tournament.rounds = [[Match(**match_data) for match_data in round_matches] for round_matches in
                                 tournament_data['rounds']]
            all_tournaments.append(tournament)
        return all_tournaments

    @staticmethod
    def get_tournament_details(tournament_name, file_path):
        """Get the name and dates of a specific tournament."""
        tournaments = Tournament.get_all_tournaments(file_path)
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return tournament
        return None

    @staticmethod
    def get_players_in_tournament_sorted(tournament_name):
        """Get a list of players in a tournament, sorted alphabetically."""
        tournament = Tournament.get_tournament_details(tournament_name, "../data/tournaments.json")
        if tournament:
            players = tournament.players
            sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
            return sorted_players
        else:
            return "Tournoi non trouvé."

    @staticmethod
    def get_tournament_rounds_and_matches(tournament_name):
        """Get a list of all rounds and matches in a tournament."""
        tournament = Tournament.get_tournament_details(tournament_name, "../data/tournaments.json")
        if tournament:
            rounds_and_matches = []
            for _round in tournament.rounds:
                round_info = f"Round: {_round.name}\n"
                matches_info = ""
                for match in _round.matches:
                    matches_info += f"{match}\n"
                rounds_and_matches.append(round_info + matches_info)
            return rounds_and_matches
        else:
            return "Tournoi non trouvé"
