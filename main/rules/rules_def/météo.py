from main.rules.rule import Rule
from main.score.score import Score
import random

class Orage(rule.Rule):

    def __init__(self):
        super().__init__("Orage", "tout le monde perds des points" )


    def onAdd(self):
        perte = random.randint(1,10)
        point_perdu = min(perte, Score.basePoints)
        super().on_add(point_perdu)
