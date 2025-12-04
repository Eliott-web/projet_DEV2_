from .. import rule
from score.score import Score
class score2x(rule.Rule):

    def __init__(self):
        super().__init__("Score x2", "Double les points gagnés")

    def on_add(self):
        Score.baseAddPoints *= 2
        super().on_add()

    def on_remove(self):
        Score.baseAddPoints *= 0.5
        super().on_remove()

    