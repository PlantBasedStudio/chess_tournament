class Match:
    """Represents a match between two players."""

    def __init__(self, player1, player2):
        """
        Initialize a match.

        Args:
            player1 (Player): The first player in the match.
            player2 (Player): The second player in the match.
        """
        self.players = [player1, player2]
        self.scores = [0, 0]  # Scores initialized to 0 for both players

    def set_score(self, player_index, score):
        """
        Set the score for a player in the match.

        Args:
            player_index (int): The index of the player (0 or 1).
            score (int): The score of the player.
        """
        self.scores[player_index] = score

    def get_players(self):
        """
        Get the players in the match.

        Returns:
            list: A list containing the players in the match.
        """
        return self.players

    def get_scores(self):
        """
        Get the scores of the players in the match.

        Returns:
            list: A list containing the scores of the players in the match.
        """
        return self.scores
