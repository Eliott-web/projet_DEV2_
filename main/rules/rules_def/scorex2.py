from main.rules.rule import Rule
from main.rules.rule_list import add_rule
from main.score.score import Score
class score2x(Rule):

    def __init__(self):
        super().__init__("Score x2", "Double les points gagnés")

    def on_add(self):
        Score.baseAddPoints *= 2
        super().on_add()

    def on_remove(self):
        Score.baseAddPoints *= 0.5
        super().on_remove()

add_rule(score2x())