from main.game_manager.mini_game.mini_game_utils import getMiniGameList
from main.rules.rule import Rule


class MiniGameRule(Rule):
    def __init__(self):
        super().__init__("MINI JEU ATTENTION", "un mini jeux se lance direct")

    def on_add(self):
        pass


    def on_remove(self):
        pass

    ##je termine le code apres ou demain