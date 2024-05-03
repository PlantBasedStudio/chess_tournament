from controllers.GameController import GameController
from controllers.TournamentController import TournamentController


def add_player():
    # controller qui appelle la vue, envoie les données au modèle, renvoi le resultat en vue.
    chess_id = input("Entrez l'identifiant du joueur : ")
    last_name = input("Entrez le nom du joueur : ")
    first_name = input("Entrez le prénom du joueur : ")
    date_of_birth = input("Entrez la date de naissance du joueur (YYYY-MM-DD) : ")
    elo = int(input("Entrez le classement ELO du joueur : "))
    player = GameController.create_player(chess_id, last_name, first_name, date_of_birth, elo)
    if player:
        print("Le joueur a été ajouté avec succès !")
    else:
        print("Une erreur s'est produite lors de l'ajout du joueur.")


def display_players():
    file_path = "../data/players.json"
    players = TournamentController.get_all_players_sorted(file_path)
    if players:
        print("Liste des joueurs :")
        for player in players:
            print(f"{player.first_name} {player.last_name} (ID: {player.chess_id}, ELO: {player.elo})")
    else:
        print("Aucun joueur trouvé.")


def create_tournament():
    name = input("Entrez le nom du tournoi : ")
    location = input("Entrez le lieu du tournoi : ")
    start_date = input("Entrez la date de début du tournoi (YYYY-MM-DD) : ")
    end_date = input("Entrez la date de fin du tournoi (YYYY-MM-DD) : ")
    num_rounds = int(input("Entrez le nombre de rounds du tournoi : "))
    tournament = GameController.create_tournament(name, location, start_date, end_date, num_rounds)
    if tournament:
        print("Le tournoi a été créé avec succès !")
    else:
        print("Une erreur s'est produite lors de la création du tournoi.")


def display_tournaments():
    file_path = "../data/tournaments.json"
    tournaments = TournamentController.get_all_tournaments(file_path)
    if tournaments:
        print("Liste des tournois :")
        for tournament in tournaments:
            print(f"{tournament.name} ({tournament.start_date} - {tournament.end_date})")
    else:
        print("Aucun tournoi trouvé.")


def display_tournament_details():
    tournament_name = input("Entrez le nom du tournoi : ")
    details = TournamentController.get_tournament_details(tournament_name)
    if details:
        print(details)
    else:
        print("Le tournoi spécifié n'a pas été trouvé.")


def manage_players_menu():
    while True:
        print("\nMenu Gérer les Joueurs:")
        print("1. Ajouter un joueur")
        print("2. Afficher la liste des joueurs")
        print("3. Retourner au menu principal")

        choice = input("Choisissez une option : ")

        if choice == "1":
            add_player()
        elif choice == "2":
            display_players()
        elif choice == "3":
            return
        else:
            print("Option invalide. Veuillez choisir une option valide.")


def manage_tournaments_menu():
    while True:
        print("\nMenu Gérer les Tournois:")
        print("1. Créer un nouveau tournoi")
        print("2. Afficher la liste des tournois")
        print("3. Afficher les détails d'un tournoi spécifique")
        print("4. Retourner au menu principal")

        choice = input("Choisissez une option : ")

        if choice == "1":
            create_tournament()
        elif choice == "2":
            display_tournaments()
        elif choice == "3":
            display_tournament_details()
        elif choice == "4":
            return
        else:
            print("Option invalide. Veuillez choisir une option valide.")


def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Quitter le programme")

        choice = input("Choisissez une option : ")

        if choice == "1":
            manage_players_menu()
        elif choice == "2":
            manage_tournaments_menu()
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez choisir une option valide.")


