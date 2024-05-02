from models.Player import Player
from models.Tournament import Tournament


class TournamentController:
    """Controls the tournament-related operations."""

    def __init__(self):
        pass

    @staticmethod
    def get_all_players_sorted():
        """Get a list of all players sorted alphabetically."""
        file_path = "../data/players.json"
        sorted_players = Player.get_all_players_sorted(file_path)
        return sorted_players

    @staticmethod
    def get_all_tournaments():
        """Get a list of all tournaments."""
        file_path = "../data/tournaments.json"
        tournaments = Tournament.get_all_tournaments(file_path)
        return tournaments

    @staticmethod
    def get_tournament_details(tournament_name):
        """Get the name and dates of a specific tournament."""
        tournament = Tournament.get_tournament_details(tournament_name)
        if tournament:
            return (f"Tournament: {tournament.name}\nStart Date: {tournament.start_date}\nEnd Date:"
                    f" {tournament.end_date}")
        else:
            return "Tournament not found."

    @staticmethod
    def get_players_in_tournament_sorted(tournament_name):
        """Get a list of players in a tournament, sorted alphabetically."""
        tournament = Tournament.get_tournament_details(tournament_name)
        if tournament:
            players = tournament.players
            sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
            return sorted_players
        else:
            return "Tournament not found."

    @staticmethod
    def get_tournament_rounds_and_matches(tournament_name):
        """Get a list of all rounds and matches in a tournament."""
        tournament = Tournament.get_tournament_details(tournament_name)
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
            return "Tournament not found."
