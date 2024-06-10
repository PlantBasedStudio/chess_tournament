import json
import os


class Player:
    """Represents a chess player."""

    def __init__(self, chess_id, last_name, first_name, date_of_birth, elo, points=0):
        """
        Initialize a player.

        Args:
            chess_id (int): The chess ID of the player.
            last_name (str): The last name of the player.
            first_name (str): The first name of the player.
            date_of_birth (str): The date of birth of the player in the format 'YYYY-MM-DD'.
            elo (int): elo of the player.
            points : points of the player.
        """

        self.chess_id = chess_id
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.elo = elo
        self.points = points

    @classmethod
    def create_player(cls, chess_id, last_name, first_name, date_of_birth, elo):
        """
        Create a new player instance.

        Args:
            chess_id (int): The chess ID of the player.
            last_name (str): The last name of the player.
            first_name (str): The first name of the player.
            date_of_birth (str): The date of birth of the player in the format 'YYYY-MM-DD'.
            elo (int): elo of the player.

        Returns:
            Player: A new Player instance.
        """
        return cls(chess_id, last_name, first_name, date_of_birth, elo)

    @staticmethod
    def get_player_by_id(chess_id):
        """Get a player by their ID."""
        # Load all players from the JSON file
        data_dir = './data'
        players_file = 'players.json'
        file_path = os.path.join(data_dir, players_file)
        players = Player.load_from_json(file_path)

        # Search for the player by ID
        for player in players:
            if player.chess_id == chess_id:
                print("informations joueurs", player.to_json())
                return player.to_json()

        # Return None if player not found
        return None

    @staticmethod
    def from_json(data):
        return Player(
            data.get('chess_id', ''),
            data.get('last_name', ''),
            data.get('first_name', ''),
            data.get('date_of_birth', ''),
            data.get('elo', 0),
            data.get('points', 0)
        )

    @classmethod
    def save_to_json(cls, player):
        """
        Save player data to a JSON file.

        Args:
            player (Player): The player instance to save.

        Raises:
            FileNotFoundError: If the data directory or players.json file does not exist.
        """
        data_dir = './data'
        players_file = 'players.json'
        file_path = os.path.join(data_dir, players_file)

        # Create the data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Check if the players.json file exists
        if not os.path.exists(file_path):
            # Create an empty players list if the file doesn't exist
            players_data = []
        else:
            # Load existing player data from the JSON file
            with open(file_path, 'r') as json_file:
                players_data = json.load(json_file)

        # Append the new player data to the list
        players_data.append(player.to_json())

        # Save the updated player data back to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(players_data, json_file, indent=4)

    def to_json(self):
        """
        Convert the player object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the player object.
        """
        return {
            'chess_id': self.chess_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'date_of_birth': self.date_of_birth,
            'elo': self.elo,
            'points': self.points
        }

    @classmethod
    def load_from_json(cls, file_path):
        """
        Load player data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            list: A list of Player instances loaded from the JSON data.
        """
        with open(file_path, 'r') as json_file:
            player_data = json.load(json_file)
        return [cls(**data) for data in player_data]

    @staticmethod
    def get_all_players_sorted(file_path):
        """Get a list of all players sorted alphabetically."""
        players = Player.load_from_json(file_path)
        sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
        return sorted_players

    def add_points(self, points):
        """Add points to the player's total."""
        self.points += points

    def get_points(self):
        """Get the player's current points."""
        return self.points
