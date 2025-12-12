from main.plateau.die.die import lancer_de
from main.rules.rules_def.malus_de import MalusDe # adapte le chemin à ton projet


regle = MalusDe()

de_normal = lancer_de()
print(f"Lancer de dé normal : {de_normal}")


valeur_appliquee = regle.on_add()
print(f"Dé après activation de MalusDe : {valeur_appliquee}")


valeur_restaurée = regle.on_remove()
print(f"Dé après désactivation de MalusDe : {valeur_restaurée}")
