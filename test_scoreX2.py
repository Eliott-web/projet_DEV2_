from main.score.score import Score
from main.rules.rules_def.scorex2 import score2x # adapte le chemin selon ton projet

# Valeur de départ
Score.baseAddPoints = 10
print("Avant la règle :", Score.baseAddPoints)

# Crée l'instance de Score2x
regle = score2x()

# Exécute la règle
regle.on_add()

# Vérifie que le score a bien été doublé
print("Après exécution de Score x2 :", Score.baseAddPoints)
