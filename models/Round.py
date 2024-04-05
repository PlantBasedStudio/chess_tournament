import random
from datetime import datetime
from models.Match import Match


class Round:
    """Represents a round in a tournament."""

    def __init__(self, name):
        """
        Initialize a round.

        Args:
            name (str): The name of the round.
        """
        self.name = name
        self.start_time = None
        self.end_time = None
        self.matches = []

    def start(self):
        """Start the round."""
        self.start_time = datetime.now()

    def end(self):
        """End the round."""
        self.end_time = datetime.now()

    def add_matches(self, matches):
        """
        Add matches to the round.

        Args:
            matches (list): List of Match instances to add to the round.
        """
        self.matches.extend(matches)

    @staticmethod
    def generate_matches(players):
        """
        Generate matches for the round based on player standings.

        Args:
            players (list): A list of Player instances sorted by standings.

        Returns:
            list: A list of Match instances representing the matches for the round.
        """
        matches = []
        # Shuffle players for fairness in case of equal standings
        random.shuffle(players)

        # Pair players based on standings
        num_players = len(players)
        for i in range(0, num_players, 2):
            match = Match(players[i], players[i + 1])
            matches.append(match)

        return matches

    def get_matches(self):
        """
        Get the matches in the round.

        Returns:
            list: A list containing the matches in the round.
        """
        return self.matches
