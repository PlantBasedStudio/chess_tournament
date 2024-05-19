from views.menu import MenuView
from controllers.TournamentController import TournamentController
from controllers.PlayerController import PlayerController
from models.Player import Player


class GameController:
    """Controller class for managing interactions between models and views."""

    @staticmethod
    def play_tournament():
        tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        tournament = GameController.find_or_create_tournament(tournament_name)

        if tournament:
            GameController.register_players(tournament)
            GameController.play_rounds(tournament)
            GameController.save_tournament(tournament)
            MenuView.display_message("Le tournoi est terminé !")
        else:
            MenuView.display_message("Le tournoi spécifié n'a pas été trouvé.")

    @staticmethod
    def find_or_create_tournament(tournament_name):
        tournaments = TournamentController.get_all_tournaments()
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return tournament
        return TournamentController.load_tournament(tournament_name, "./data/tournaments.json")

    @staticmethod
    def register_players(tournament):
        num_players = 2 * tournament.num_rounds
        if tournament.current_round == 1:
            MenuView.display_message("Inscrivez-vous au tournoi :")
            while len(tournament.registered_players) < num_players:
                player_id = MenuView.get_user_input("Entrez l'identifiant du joueur : ")
                player = GameController.find_or_create_player(player_id)
                if player:
                    if player not in tournament.registered_players:
                        tournament.registered_players.append(player)
                        print('plus que', num_players - len(tournament.registered_players), 'joueurs à inscrire')
                    else:
                        MenuView.display_message("Ce joueur est déjà inscrit au tournoi.")
                else:
                    PlayerController.add_player()

    @staticmethod
    def find_or_create_player(player_id):
        return Player.get_player_by_id(player_id)

    @staticmethod
    def play_rounds(tournament):
        while tournament.current_round <= tournament.num_rounds:
            MenuView.display_message(f"Tournoi en cours : {tournament.name}, Round {tournament.current_round}")
            matches = GameController.generate_matches(tournament.registered_players)
            GameController.record_match_results(matches)
            winners = GameController.determine_winners(matches)
            tournament.registered_players = winners

    @staticmethod
    def generate_matches(players):
        matches = []
        players_copy = players.copy()
        while len(players_copy) >= 2:
            player1 = players_copy.pop(0)
            player2 = players_copy.pop(0)
            matches.append((player1, player2))
        return matches

    @staticmethod
    def record_match_results(matches):
        for match in matches:
            result = MenuView.get_user_input(f"Entrez le résultat du match entre {match[0].first_name} "
                                             f"{match[0].last_name} et {match[1].first_name} "
                                             f"{match[1].last_name} (0 pour match nul, 1 pour victoire "
                                             f"du premier joueur, 2 pour victoire du second joueur) : ")
            GameController.update_points(match, result)

    @staticmethod
    def update_points(match, result):
        if result == '0':
            match[0].points += 0.5
            match[1].points += 0.5
        elif result == '1':
            match[0].points += 1
        elif result == '2':
            match[1].points += 1

    @staticmethod
    def determine_winners(matches):
        winners = []
        draw_matches = []
        for match in matches:
            if match[0].points > match[1].points:
                winners.append(match[0])
            elif match[1].points > match[0].points:
                winners.append(match[1])
            else:
                draw_matches.append(match)
        winners.extend(GameController.resolve_draws(draw_matches))
        return winners

    @staticmethod
    def resolve_draws(draw_matches):
        resolved_winners = []
        for match in draw_matches:
            player1, player2 = match
            result = MenuView.get_user_input(f"Entrez le résultat du match entre {player1.first_name} "
                                             f"{player1.last_name} et {player2.first_name} "
                                             f"{player2.last_name} (0 pour match nul, 1 pour victoire "
                                             f"du premier joueur, 2 pour victoire du second joueur) : ")
            GameController.update_points(match, result)
            resolved_winners.append(player1 if player1.points > player2.points else player2)
        return resolved_winners

    @staticmethod
    def save_tournament(tournament):
        TournamentController.save_tournament(tournament, "./data/tournaments.json")
