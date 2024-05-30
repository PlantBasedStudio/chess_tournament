import random

from views.menu import MenuView
from controllers.TournamentController import TournamentController


class GameController:
    """Controller class for managing interactions between models and views."""

    previous_matches = set()

    @staticmethod
    def play_tournament():
        tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        tournament = TournamentController.find_or_create_tournament(tournament_name)

        if tournament:
            TournamentController.register_players(tournament)
            TournamentController.play_rounds(tournament)
            TournamentController.save_tournament(tournament)
            print(
                f"Tournoi '{tournament.name}' sauvegardé avec {len(tournament.registered_players)} joueurs enregistrés.")
            MenuView.display_message("Le tournoi est terminé !")
        else:
            MenuView.display_message("Le tournoi spécifié n'a pas été trouvé.")



    @staticmethod
    def generate_matches(players):
        matches = []
        players_copy = players.copy()
        random.shuffle(players_copy)

        while len(players_copy) >= 2:
            player1 = players_copy.pop(0)
            player2 = players_copy.pop(0)

            match = (player1['chess_id'], player2['chess_id'])
            reversed_match = (player2['chess_id'], player1['chess_id'])

            # Check if match or its reverse has already happened
            while match in GameController.previous_matches or reversed_match in GameController.previous_matches:
                players_copy.append(player2)  # Put player2 back and try with the next one
                if len(players_copy) < 2:
                    # Not enough players left to form a new match
                    return matches
                player2 = players_copy.pop(0)
                match = (player1['chess_id'], player2['chess_id'])
                reversed_match = (player2['chess_id'], player1['chess_id'])

            # Add the new match to the list and to the set of previous matches
            matches.append({'player1': player1, 'player2': player2})
            GameController.previous_matches.add(match)

        return matches




