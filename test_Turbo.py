from main.rules.rules_def.Turbo_tchikita import TurBo
from main.plateau.die.die import lancer_de

# Lancer de départ
valeur_normale = lancer_de()
print("Valeur du dé normale :", valeur_normale)

# Crée l'instance de Turbo
regle = TurBo()

# Active la règle (multiplie par 2)
valeur_turbo = regle.on_add()
print("Valeur du dé avec Turbo :", valeur_turbo)

# Désactive la règle (divise par 2)
valeur_apres_removal = regle.on_remove()
print("Valeur du dé après désactivation :", valeur_apres_removal)
