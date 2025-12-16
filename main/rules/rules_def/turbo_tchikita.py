from main.rules.rule import Rule
from main.plateau.die.die import lancer_de


class Turbo(Rule):

    def __init__(self):
        super().__init__("Turbo tchikita","vous avancez en X2")
    def on_add(self):
        from main.main_loop import plateau_menu
        plateau_menu.case_multiplicateur = 2

    def on_remove(self):
        from main.main_loop import plateau_menu
        plateau_menu.case_multiplicateur = 1

