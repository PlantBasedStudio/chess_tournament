from models.Player import Player
from models.Tournament import Tournament
from models.Round import Round
from models.Match import Match


class GameController:
    """Controller class for managing interactions between models and views."""

    @staticmethod
    def create_player(chess_id, last_name, first_name, date_of_birth, elo):
        """Create a new player."""
        return Player.create_player(chess_id, last_name, first_name, date_of_birth, elo)

    @staticmethod
    def create_tournament(name, location, start_date, end_date, num_rounds=4, current_round=1, players=None):
        """Create a new tournament."""
        return Tournament(name, location, start_date, end_date, num_rounds, current_round, players)

    @staticmethod
    def create_round(name):
        """Create a new round."""
        return Round(name)

    @staticmethod
    def create_match(player1, player2):
        """Create a new match between two players."""
        return Match(player1, player2)