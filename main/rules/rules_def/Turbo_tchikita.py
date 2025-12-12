from main.rules.rule import Rule
from main.plateau.die.die import lancer_de


class Turbo(Rule):

    def __init__(self):
        super().__init__("Turbo tchikita","vous avancez en X2")
        self.valeur_de = 0
    def on_add(self):
        de = lancer_de()
        self.valeur_de = de*2
        super().on_add()
        return self.valeur_de
    def on_remove(self):
       valeur_de = lancer_de() *0.5
       super().on_remove()
       return valeur_de
