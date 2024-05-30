from views.menu import MenuView
from models.Tournament import Tournament
from models.Round import Round
from controllers.PlayerController import PlayerController


class TournamentController:
    """Controls the tournament-related operations."""

    @staticmethod
    def create_tournament():
        """Create a new tournament."""
        name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        location = MenuView.get_user_input("Entrez le lieu du tournoi : ")
        start_date = MenuView.get_user_input("Entrez la date de début du tournoi (YYYY-MM-DD) : ")
        end_date = MenuView.get_user_input("Entrez la date de fin du tournoi (YYYY-MM-DD) : ")
        num_rounds = int(MenuView.get_user_input("Entrez le nombre de rounds du tournoi : "))
        tournament = Tournament(name, location, start_date, end_date, num_rounds, description="")
        TournamentController.save_tournament(tournament)
        if tournament:
            MenuView.display_message("Le tournoi a été créé avec succès !")
        else:
            MenuView.display_message("Une erreur s'est produite lors de la création du tournoi.")

    @staticmethod
    def display_tournaments():
        """Display the list of tournaments."""
        tournaments = TournamentController.get_all_tournaments()
        if tournaments:
            MenuView.display_message("Liste des tournois :")
            for tournament in tournaments:
                MenuView.display_message(f"{tournament.name} ({tournament.start_date} - {tournament.end_date})")
        else:
            MenuView.display_message("Aucun tournoi trouvé.")

    @staticmethod
    def display_tournament_details():
        """Display the details of a specific tournament."""
        tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        details = TournamentController.get_tournament_details(tournament_name)
        if details:
            MenuView.display_message(details)
        else:
            MenuView.display_message("Le tournoi spécifié n'a pas été trouvé.")

    @staticmethod
    def save_tournament(tournament, file_path="./data/tournaments.json"):
        """
        Save the tournament data to a JSON file.

        Args:
            tournament (Tournament): The tournament instance to save.
            file_path (str): The path to the JSON file.
        """
        tournament.save_to_json(file_path)

    @staticmethod
    def load_tournament(tournament_name, file_path="./data/tournaments.json"):
        """
        Load tournament data from a JSON file.

        Args:
            tournament_name(str): The name of the tournament.
            file_path (str): The path to the JSON file.

        Returns:
            Tournament: A Tournament instance loaded from the JSON data.
        """
        return Tournament.load_tournament(tournament_name, file_path)

    @staticmethod
    def find_or_create_tournament(tournament_name):
        tournaments = TournamentController.get_all_tournaments()
        for tournament in tournaments:
            if tournament.name == tournament_name:
                return tournament
        return TournamentController.load_tournament(tournament_name)

    @staticmethod
    def register_players(tournament):
        num_players = 2 * tournament.num_rounds
        if tournament.current_round == 1:
            MenuView.display_message("Inscrivez-vous au tournoi :")
            while len(tournament.registered_players) < num_players:
                player_id = MenuView.get_user_input("Entrez l'identifiant du joueur : ")
                player = PlayerController.find_or_create_player(player_id)
                if player:
                    if player not in tournament.registered_players:
                        tournament.registered_players.append(player)
                        print("Joueur ajouté, liste:", tournament.registered_players)
                        print('plus que', num_players - len(tournament.registered_players), 'joueurs à inscrire')
                    else:
                        MenuView.display_message("Ce joueur est déjà inscrit au tournoi.")
                else:
                    MenuView.display_message("Joueur non trouvé. Veuillez ajouter le joueur d'abord.")
                    PlayerController.add_player()

    @staticmethod
    def play_rounds(tournament):
        tournament_winners = []  # Liste pour stocker les gagnants de chaque tour
        while tournament.current_round <= tournament.num_rounds:
            round_name = f"Round {tournament.current_round}"
            current_round = Round(round_name)
            current_round.start()

            MenuView.display_message(f"Tournoi en cours : {tournament.name}, {current_round.name}")
            matches = Round.generate_matches(tournament.registered_players)
            TournamentController.record_match_results(tournament, current_round, matches)
            winners = TournamentController.determine_winners(matches)
            tournament_winners.append(winners)  # Ajouter les gagnants de ce tour à la liste
            tournament.current_round += 1

        # Déterminer le gagnant final du tournoi
        final_winner = TournamentController.determine_tournament_winner(tournament_winners)
        tournament.winner = final_winner
        MenuView.display_message(
            f"Gagnant final du tournoi {tournament.name}: {final_winner['first_name']} {final_winner['last_name']}")

    @staticmethod
    def determine_tournament_winner(tournament_winners):
        final_winner = None
        max_points = float('-inf')  # Initialisation avec une valeur très basse

        for winners in tournament_winners:
            for winner in winners:
                # Vérifier si le dictionnaire contient la clé 'points'
                if 'points' in winner:
                    points = winner['points']
                    if points > max_points:
                        final_winner = winner
                        max_points = points

        return final_winner

    @staticmethod
    def record_match_results(tournament, current_round, matches):
        round_results = []
        current_round_index = tournament.get_current_round_index()
        for match in matches:
            player1, player2 = match.get_players()
            result = MenuView.get_user_input(
                f"Entrez le résultat du match entre {player1['first_name']} {player1['last_name']} "
                f"et {player2['first_name']} {player2['last_name']} (0 pour match nul, 1 pour victoire "
                f"du premier joueur, 2 pour victoire du second joueur) : "
            )
            if result in ['0', '1', '2']:
                match.set_score(0, int(result))  # Met à jour le score du premier joueur
                match.set_score(1, int(not int(result)))  # Met à jour le score du second joueur
                TournamentController.update_points(match, result)  # Met à jour les points des joueurs
                winner = player1 if result == '1' else (player2 if result == '2' else None)
                round_results.append({
                    "player1": {"chess_id": player1["chess_id"], "score": int(result)},
                    "player2": {"chess_id": player2["chess_id"], "score": int(not int(result))},
                    "winner": winner
                })
                current_round.add_matches(matches)
            else:
                MenuView.display_message("Veuillez entrer un résultat valide.")
        tournament.add_round_results(current_round_index, round_results)  # Ajouter les résultats du tour au tournoi

    @staticmethod
    def update_points(match, result):
        player1, player2 = match.get_players()

        # Vérifiez si les points sont déjà présents dans les dictionnaires,
        # sinon initialisez-les à zéro
        player1_points = player1.get('points', 0)
        player2_points = player2.get('points', 0)

        if result == '0':
            player1['points'] = player1_points + 0.5
            player2['points'] = player2_points + 0.5
        elif result == '1':
            player1['points'] = player1_points + 1
        elif result == '2':
            player2['points'] = player2_points + 1

    @staticmethod
    def determine_winners(matches):
        winners = []
        for match in matches:
            player1, player2 = match.get_players()
            scores = match.get_scores()
            if scores[0] > scores[1]:
                winners.append(player1)
            elif scores[1] > scores[0]:
                winners.append(player2)
        return winners

    @staticmethod
    def get_all_tournaments(file_path="./data/tournaments.json"):
        """
        Get a list of all tournaments.

        Returns:
            list: A list of Tournament instances.
        """
        return Tournament.get_all_tournaments(file_path)

    @staticmethod
    def get_tournament_details(tournament_name):
        """Get the name and dates of a specific tournament."""
        file_path = "./data/tournaments.json"
        tournaments = Tournament.get_all_tournaments(file_path)
        for tournament in tournaments:
            if tournament.name == tournament_name:
                if tournament.current_round <= tournament.num_rounds:
                    return "Le tournoi n'est pas encore terminé."

                tournament_info = (f"Tournament: {tournament.name}\nStart Date: {tournament.start_date}\nEnd Date:"
                                   f" {tournament.end_date}\nRegistered Players:\n")
                for player in tournament.registered_players:
                    first_name = player.first_name if hasattr(player, 'first_name') else 'Unknown'
                    last_name = player.last_name if hasattr(player, 'last_name') else 'Unknown'
                    chess_id = player.chess_id if hasattr(player, 'chess_id') else 'Unknown'
                    tournament_info += f"  - {first_name} {last_name} ({chess_id}),\n"

                # Check if there is a winner
                if tournament.winner:
                    tournament_info += f"Tournament Winner: {tournament.winner.get('first_name', 'Unknown')} " \
                                       f"{tournament.winner.get('last_name', 'Unknown')} " \
                                       f"({tournament.winner.get('chess_id', 'Unknown')})"
                else:
                    tournament_info += "Tournament Winner: None"

                return tournament_info

        return "Aucun tournoi trouvé."
