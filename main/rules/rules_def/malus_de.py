from main.plateau.die.die import lancer_de
from main.rules.rule import Rule

class MalusDe(Rule):
    def __init__(self):
        super().__init__("Malus Dé", "Vous ne pouvez avancer que d'une case")
        self.valeur_de_modifiee = 0

    def on_add(self):

        de = lancer_de()
        self.valeur_de_modifiee = min(de, 1)

        super().on_add()
        return self.valeur_de_modifiee

    def on_remove(self):
        de_rejoue = lancer_de()
        self.valeur_de_modifiee = 0
        super().on_remove()
        return de_rejoue