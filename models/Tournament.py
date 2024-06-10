import json
import os
from models.Player import Player
from models.Round import Round


class Tournament:
    """Represents a chess tournament."""

    def __init__(self, name, location, start_date, end_date, num_rounds=4, current_round=1,
                 description="", winner=None):
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
        self.winner = winner

    def add_round_results(self, round_index, round_results):
        self.rounds[round_index] = round_results

    def get_current_round_index(self):
        return self.current_round - 1

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
            "registered_players": [player.to_json() if isinstance(player, Player)
                                   else player for player in self.registered_players],
            "winner": self.winner.to_json() if self.winner and isinstance(self.winner, Player) else self.winner,
            "rounds": [[{
                "player1": match["player1"],
                "player2": match["player2"],
                "winner": match.get("winner")
            } for match in round_matches] for round_matches in self.rounds]
        }

        print("Données du tournoi :", tournament_data)
        # Load existing tournament data from the JSON file
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                all_tournaments = json.load(json_file)
        else:
            all_tournaments = []

        # Find and replace the tournament if it exists, otherwise append
        tournament_exists = False
        for i, existing_tournament in enumerate(all_tournaments):
            if existing_tournament['name'] == self.name:
                all_tournaments[i] = tournament_data
                tournament_exists = True
                break

        if not tournament_exists:
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
                    tournament_data.get('name', ''),
                    tournament_data.get('location', ''),
                    tournament_data.get('start_date', ''),
                    tournament_data.get('end_date', ''),
                    tournament_data.get('num_rounds', 0),
                    tournament_data.get('current_round', 0),
                    tournament_data.get('description', ''),
                    tournament_data.get('winner', None)
                )
                tournament.registered_players = [Player.from_json(player) if isinstance(player, dict)
                                                 else player
                                                 for player in tournament_data.get('registered_players', [])]
                tournament.rounds = tournament_data.get('rounds', [])
                return tournament

        return None

    @staticmethod
    def get_all_tournaments(file_path="./data/tournaments.json"):
        tournaments = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                tournaments = [Tournament.from_dict(t) for t in data]
        return tournaments

    @staticmethod
    def set_all_tournaments(tournaments, file_path="./data/tournaments.json"):
        data = [tournament.to_dict() for tournament in tournaments]
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "registered_players": [player.to_json() for player in self.registered_players],
            "winner": self.winner.to_json() if self.winner else None
        }

    @staticmethod
    def from_dict(data):
        tournament = Tournament(
            data["name"], data["location"], data["start_date"], data["end_date"],
            data["num_rounds"], description=""
        )
        tournament.current_round = data["current_round"]
        tournament.registered_players = [Player.from_json(p) for p in data["registered_players"]]
        tournament.winner = Player.from_json(data["winner"]) if data["winner"] else None
        return tournament

    @staticmethod
    def get_tournament_details(tournament_name, file_path):
        """Get the name and dates of a specific tournament."""
        tournaments = Tournament.get_all_tournaments(file_path)
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return tournament
        return None
