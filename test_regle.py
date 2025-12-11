from main.rules.rule_list import load_rules, get_random_rule, run_rule

# Charger toutes les règles
load_rules()

# Tirer et exécuter une règle aléatoire
rule = get_random_rule()
run_rule(rule)
