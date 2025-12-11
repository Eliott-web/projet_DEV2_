from rule_list import load_rules, list_rules, get_random_rule, run_rule

# 1. Charger toutes les règles
load_rules()

# 2. Vérifier que toutes les règles sont bien chargées
print("Toutes les règles chargées :")
for i, r in enumerate(list_rules, 1):
    print(f"{i}. {r._name} - {r._description}")

# 3. Récupérer et exécuter une règle aléatoire
print("\nExécution d'une règle aléatoire :")
rule = get_random_rule()
run_rule(rule)
