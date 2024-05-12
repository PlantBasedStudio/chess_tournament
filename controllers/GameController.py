from models.Tournament import Tournament
from views.menu import MenuView
from controllers.TournamentController import TournamentController
from models.Player import Player
import random

class GameController:
    """Controller class for managing interactions between models and views."""

    @staticmethod
    def run():
        while True:
            MenuView.display_main_menu()
            choice = MenuView.get_user_input("Choisissez une option : ")

            if choice == "1":
                GameController.manage_players_menu()
            elif choice == "2":
                GameController.manage_tournaments_menu()
            elif choice == "3":
                MenuView.display_message("Au revoir !")
                break
            else:
                MenuView.display_message("Option invalide. Veuillez choisir une option valide.")

    @staticmethod
    def manage_players_menu():
        while True:
            MenuView.display_manage_players_menu()
            choice = MenuView.get_user_input("Choisissez une option : ")

            if choice == "1":
                GameController.add_player()
            elif choice == "2":
                GameController.display_players()
            elif choice == "3":
                break
            else:
                MenuView.display_message("Option invalide. Veuillez choisir une option valide.")

    @staticmethod
    def manage_tournaments_menu():
        while True:
            MenuView.display_manage_tournaments_menu()
            choice = MenuView.get_user_input("Choisissez une option : ")

            if choice == "1":
                GameController.create_tournament()
            elif choice == "2":
                GameController.display_tournaments()
            elif choice == "3":
                GameController.display_tournament_details()
            elif choice == "4":
                GameController.play_tournament()
            elif choice == "5":
                break
            else:
                MenuView.display_message("Option invalide. Veuillez choisir une option valide.")

    @staticmethod
    def add_player():
        """Add a player to the tournament."""
        chess_id = MenuView.get_user_input("Entrez l'identifiant du nouveau joueur à créer : ")

        # Check if the player already exists
        existing_player = Player.get_player_by_id(chess_id)

        if existing_player:
            MenuView.display_message("Le joueur existe déjà !")
            player = existing_player
        else:
            last_name = MenuView.get_user_input("Entrez le nom du joueur : ")
            first_name = MenuView.get_user_input("Entrez le prénom du joueur : ")
            date_of_birth = MenuView.get_user_input("Entrez la date de naissance du joueur (YYYY-MM-DD) : ")
            elo = int(MenuView.get_user_input("Entrez le classement ELO du joueur : "))
            player = Player.create_player(chess_id, last_name, first_name, date_of_birth, elo)
            if player:
                Player.save_to_json(player)
                MenuView.display_message("Le joueur a été ajouté avec succès !")
            else:
                MenuView.display_message("Une erreur s'est produite lors de l'ajout du joueur.")


    @staticmethod
    def display_players():
        """Display the list of players."""
        file_path = "./data/players.json"
        players = Player.get_all_players_sorted(file_path)
        if players:
            MenuView.display_message("Liste des joueurs :")
            for player in players:
                MenuView.display_message(f"{player.first_name} {player.last_name} (ID: {player.chess_id}, ELO: {player.elo})")
        else:
            MenuView.display_message("Aucun joueur trouvé.")

    @staticmethod
    def create_tournament():
        """Create a new tournament."""
        name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        location = MenuView.get_user_input("Entrez le lieu du tournoi : ")
        start_date = MenuView.get_user_input("Entrez la date de début du tournoi (YYYY-MM-DD) : ")
        end_date = MenuView.get_user_input("Entrez la date de fin du tournoi (YYYY-MM-DD) : ")
        num_rounds = int(MenuView.get_user_input("Entrez le nombre de rounds du tournoi : "))
        tournament = TournamentController.create_tournament(name, location, start_date, end_date, num_rounds)
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
    def play_tournament():
        tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
        tournaments = TournamentController.get_all_tournaments()
        existing_tournament = None
        for tournament in tournaments:
            if tournament.name == tournament_name:
                existing_tournament = tournament
                break

        if existing_tournament:
            tournament = existing_tournament
        else:
            # Le tournoi n'existe pas encore, donc on le crée
            tournament = TournamentController.load_tournament(tournament_name, "./data/tournaments.json")

        if tournament:
            # Déterminer le nombre de joueurs en fonction du nombre de rounds
            num_players = 2 * tournament.num_rounds

            # Si c'est le premier round, demander aux joueurs de s'inscrire
            if tournament.current_round == 1:
                MenuView.display_message("Inscrivez-vous au tournoi :")
                while len(tournament.registered_players) < num_players:
                    player_id = MenuView.get_user_input("Entrez l'identifiant du joueur : ")
                    existing_player = None

                    # Vérifier si le joueur est déjà dans la liste tournament.registered_players
                    for player in tournament.registered_players:
                        if player.chess_id == player_id:
                            existing_player = player
                            break

                    # Si le joueur n'est pas dans la liste tournament.registered_players, vérifiez dans le fichier JSON
                    if not existing_player:
                        existing_player = Player.get_player_by_id(player_id)

                    if existing_player:
                        # Vérifier si le joueur est déjà inscrit
                        if existing_player not in tournament.registered_players:
                            tournament.registered_players.append(existing_player)
                            print('plus que', num_players - len(tournament.registered_players),
                                  'joueurs a inscrire')
                        else:
                            MenuView.display_message("Ce joueur est déjà inscrit au tournoi.")
                    else:
                        GameController.add_player()

            while tournament.current_round <= tournament.num_rounds:
                MenuView.display_message(f"Tournoi en cours : {tournament_name}, Round {tournament.current_round}")

                # Générer les paires de joueurs pour les matchs du round actuel
                matches = []
                players = tournament.registered_players.copy()
                while len(players) >= 2:
                    player1 = players.pop(0)
                    player2 = players.pop(0)
                    matches.append((player1, player2))

                # Jouer les matchs et enregistrer les résultats
                for match in matches:
                    result = MenuView.get_user_input(f"Entrez le résultat du match entre {match[0].first_name} "
                                                     f"{match[0].last_name} et {match[1].first_name} "
                                                     f"{match[1].last_name} (0 pour match nul, 1 pour victoire "
                                                     f"du premier joueur, 2 pour victoire du second joueur) : ")
                    if result == '0':
                        match[0].points += 0.5
                        match[1].points += 0.5
                    elif result == '1':
                        match[0].points += 1
                    elif result == '2':
                        match[1].points += 1

                # Identifier les joueurs gagnants
                winners = []
                for match in matches:
                    if match[0].points > match[1].points:
                        winners.append(match[0])
                    elif match[1].points > match[0].points:
                        winners.append(match[1])

                # S'il y a égalité, jouer un match supplémentaire entre les joueurs concernés
                draw_matches = [match for match in matches if match[0].points == match[1].points]
                for draw_match in draw_matches:
                    player1, player2 = draw_match
                    result = MenuView.get_user_input(f"Entrez le résultat du match entre {player1.first_name} "
                                                     f"{player1.last_name} et {player2.first_name} "
                                                     f"{player2.last_name} (0 pour match nul, 1 pour victoire "
                                                     f"du premier joueur, 2 pour victoire du second joueur) : ")
                    if result == '0':
                        player1.points += 0.5
                        player2.points += 0.5
                    elif result == '1':
                        player1.points += 1
                    elif result == '2':
                        player2.points += 1
                    winners.append(player1) if player1.points > player2.points else winners.append(player2)

                # Mettre à jour les joueurs gagnants pour le prochain round
                tournament.registered_players = winners

                if not existing_tournament:
                    TournamentController.save_tournament(tournament, "./data/tournaments.json")

                # Ajoutez la sauvegarde des résultats des matchs ici
                rounds_results = []
                for i, round_matches in enumerate(tournament.rounds):
                    round_results = []
                    for match_index, match in enumerate(round_matches):
                        result = {
                            "match_number": match_index + 1,
                            "players": [match[0].chess_id, match[1].chess_id],
                            "winner": match[0].chess_id if match[0].points > match[1].points else match[1].chess_id,
                            "start_date": "",  # Ajoutez les dates de début et de fin si disponibles
                            "end_date": ""
                        }
                        round_results.append(result)
                    rounds_results.append(round_results)

                # Mettez à jour la structure des rounds avec les résultats des matchs
                for i in range(len(tournament.rounds)):
                    tournament.rounds[i] = rounds_results[i]

                # Sauvegardez le tournoi avec les résultats des matchs mis à jour
                TournamentController.save_tournament(tournament, "./data/tournaments.json")

            MenuView.display_message("Le tournoi est terminé !")
        else:
            MenuView.display_message("Le tournoi spécifié n'a pas été trouvé.")
