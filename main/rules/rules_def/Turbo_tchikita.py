from main.rules.rule import Rule
from main.plateau.die.die import lancer_de


class TurBo(Rule):

    def __init__(self):
        super().__init__("Turbo tchikita","vous avancez en X2")

    def on_add(self):
        valeur_De = lancer_de()*2
        super().on_add()
        return valeur_De
    def on_remove(self):
       valeur_de = lancer_de() *0.5
       super().on_remove()
       return valeur_de
