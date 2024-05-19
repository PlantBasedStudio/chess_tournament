from views.menu import MenuView
from models.Player import Player


class PlayerController:
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
                MenuView.display_message(
                    f"{player.first_name} {player.last_name} (ID: {player.chess_id}, ELO: {player.elo})")
        else:
            MenuView.display_message("Aucun joueur trouvé.")