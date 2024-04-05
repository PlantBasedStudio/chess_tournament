import json
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
        with open(file_path, 'w') as json_file:
            json.dump(tournament_data, json_file, indent=4)

    @classmethod
    def load_from_json(cls, file_path):
        """
        Load tournament data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            Tournament: A Tournament instance loaded from the JSON data.
        """
        with open(file_path, 'r') as json_file:
            tournament_data = json.load(json_file)
        tournament = cls(
            tournament_data['name'],
            tournament_data['location'],
            tournament_data['start_date'],
            tournament_data['end_date'],
            tournament_data['num_rounds'],
            tournament_data['current_round'],
            tournament_data['description']
        )
        tournament.registered_players = [Player(**player_data) for player_data in tournament_data['registered_players']]
        tournament.rounds = [[Match(**match_data) for match_data in round_matches]
                             for round_matches in tournament_data['rounds']]
        return tournament

    @classmethod
    def get_all_tournaments(cls, file_path):
        """
        Get a list of all tournaments.

        Args:
            file_path (str): The path to the JSON file containing tournament data.

        Returns:
            list: A list of Tournament instances.
        """
        all_tournaments = cls.load_from_json(file_path)
        return all_tournaments

    def get_tournament_details(self):
        """Get the name and dates of the tournament."""
        return f"Tournament: {self.name}\nStart Date: {self.start_date}\nEnd Date: {self.end_date}"

    def get_players_in_tournament_sorted(self):
        """Get a list of players in the tournament sorted alphabetically."""
        return sorted(self.registered_players, key=lambda player: (player.last_name, player.first_name))

    def get_all_rounds_and_matches(self):
        """Get a list of all rounds and matches in the tournament."""
        all_rounds_matches = []
        for round_ in self.rounds:
            round_info = {'round_name': round_, 'matches': []}
            for match in round_:
                match_info = {'player1': match.player1, 'player2': match.player2, 'score1': match.score1,
                              'score2': match.score2}
                round_info['matches'].append(match_info)
            all_rounds_matches.append(round_info)
        return all_rounds_matches
