from main.rules.rule import Rule
from main.score.score import Score
import random


class Orage(Rule):

    def __init__(self):
        super().__init__("Orage", "tout le monde perds des points" )
        self.points_perdu = 0

    def onAdd(self):
        perte = random.randint(1,10)
        self.points_perdu = min(perte, Score.basePoints)
        Score.basePoints -= self.points_perdu
        super().on_add()
    def onRemove(self):

        Score.basePoints -= self.points_perdu
        self.points_perdu = 0
        super().on_remove()




