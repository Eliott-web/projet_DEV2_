from main.rules.rule import Rule


class MiniGameRule(Rule):
    def __init__(self):
        super().__init__("Mini JEU HARD", "Le temps du mini-jeu est réduit à 5 secondes")
        self._original_time_limit = None

    def on_add(self):
        from main.game_manager.mini_game.mini_game import MiniGame

        self._original_time_limit = MiniGame.default_time_limit
        MiniGame.default_time_limit = 5


    def on_remove(self):
        if self._original_time_limit is not None:
            from main.game_manager.mini_game.mini_game import MiniGame
            MiniGame.default_time_limit = self._original_time_limit
