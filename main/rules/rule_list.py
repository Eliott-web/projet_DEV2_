import importlib.util
from pathlib import Path
import random
from main.rules.rule import Rule

list_rules = []
active_rule = None  # règle actuellement active
last_rule = None    # dernière règle tirée pour éviter répétition

def load_rules():

    RULES_DIR = Path(__file__).parent / "rules_def"

    for file in RULES_DIR.iterdir():
        if file.suffix == ".py" and not file.name.startswith("__"):
            module_name = file.stem
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Instancie toutes les classes héritant de Rule
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Rule) and attr is not Rule:
                    instance = attr()
                    list_rules.append(instance)  # ⚠️ on_add n'est pas appelé ici

def get_random_rule():
    """Retourne une règle aléatoire différente de la dernière tirée"""
    global last_rule

    if not list_rules:
        raise Exception("Aucune règle chargée. Appelle load_rules() d'abord.")

    if last_rule is None:
        # Premier tirage → aucune contrainte
        rule = random.choice(list_rules)
        last_rule = rule.__class__
        return rule

    # On filtre par classe et non par instance
    possible_rules = [r for r in list_rules if r.__class__ is not last_rule]

    # S'il n'y a plus d'autre règle (cas 1 règle)
    if not possible_rules:
        possible_rules = list_rules

    rule = random.choice(possible_rules)
    last_rule = rule.__class__
    return rule

def run_rule(rule):
    """Exécute une règle et désactive automatiquement l'ancienne"""
    global active_rule

    # Désactive l'ancienne règle si elle existe
    if active_rule is not None:
        print(f"Désactivation de la règle précédente : {active_rule._name}")
        active_rule.on_remove()

    # Active la nouvelle règle
    print(f"Exécution de la règle : {rule._name} - {rule._description}")
    rule.on_add()

    # Met à jour la règle active
    active_rule = rule
