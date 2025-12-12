
from main.rules.rule import Rule
class ScoreX2(Rule):

    def __init__(self):
        super().__init__("Score x2", "Double les points gagnés")

    def on_add(self):
        from main.main_loop import plateau_menu
        plateau_menu.score_multiplicateur = 2
        

    def on_remove(self):
        from main.main_loop import plateau_menu
        plateau_menu.score_multiplicateur = 1
