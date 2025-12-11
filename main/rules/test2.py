from main.score.score import Score
from main.rules.rule_list import load_rules# importe ton module Score

load_rules()  # charge toutes les règles et exécute leurs on_add()

# Vérifie que les règles ont bien modifié les variables
print("Valeur de Score.baseAddPoints après chargement des règles :", Score.baseAddPoints)

# Affiche toutes les règles chargées

