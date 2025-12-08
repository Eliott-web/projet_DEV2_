from main.game_manager.mini_game.mini_game import
from main.rules.rule import Rule


class on_life (Rule):
    def __init__(self):
        super().__init__("on_life","si vous perdez le mini jeu, vous reculez de 5 cases")

    def on_add(self):



    def on_remove(self):