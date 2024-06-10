from views.menu import MenuView
from controllers.TournamentController import TournamentController
from controllers.GameController import GameController
from controllers.PlayerController import PlayerController


class MainController:
    """Controller class for managing interactions between models and views."""

    @staticmethod
    def run():
        while True:
            MenuView.display_main_menu()
            choice = MenuView.get_user_input("Choisissez une option : ")

            if choice == "1":
                MainController.manage_players_menu()
            elif choice == "2":
                MainController.manage_tournaments_menu()
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
                PlayerController.add_player()
            elif choice == "2":
                PlayerController.display_players()
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
                TournamentController.create_tournament()
            elif choice == "2":
                TournamentController.display_tournaments()
            elif choice == "3":
                TournamentController.display_tournament_details()
            elif choice == "4":
                GameController.play_tournament()
            elif choice == "5":
                tournament_name = MenuView.get_user_input("Entrez le nom du tournoi : ")
                TournamentController.display_players_sorted(tournament_name)
            elif choice == "6":
                MenuView.display_message("Retour au menu")
                break
            else:
                MenuView.display_message("Option invalide. Veuillez choisir une option valide.")
