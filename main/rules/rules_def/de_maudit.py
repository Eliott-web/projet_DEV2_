from main.plateau.die import die
from main.rules.rule import Rule


class de_mauidit(Rule):
    def __init__(self):
        super().__init__("dé maudit", "Chaque lancer de dé vous fait reculer")

    def on_add(self):
        # On force le dé à faire 1
        die.multiplicateur = -1
        super().on_add()

    def on_remove(self):
        # On remet le dé normal
        die.multiplicateur = 1
        super().on_remove()
