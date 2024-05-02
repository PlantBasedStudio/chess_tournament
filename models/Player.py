import json


class Player:
    """Represents a chess player."""

    def __init__(self, chess_id, last_name, first_name, date_of_birth, elo):
        """
        Initialize a player.

        Args:
            chess_id (int): The chess ID of the player.
            last_name (str): The last name of the player.
            first_name (str): The first name of the player.
            date_of_birth (str): The date of birth of the player in the format 'YYYY-MM-DD'.
            elo (int): elo of the player.
        """
        self.chess_id = chess_id
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.elo = elo

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

    def to_json(self):
        """
        Convert the player object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the player object.
        """
        return {
            "chess_id": self.chess_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "elo": self.elo
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