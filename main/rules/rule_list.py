import os
import importlib.util
from pathlib import Path
import random

list_rules = []

# Classe Rule importée depuis ton fichier rule.py
from rule import Rule

def load_rules():
    """
    Importe automatiquement tous les fichiers Python du dossier rules_def
    et instancie toutes les classes héritant de Rule.
    """
    RULES_DIR = Path(__file__).parent / "rules_def"

    for file in RULES_DIR.iterdir():
        if file.suffix == ".py" and not file.name.startswith("__"):
            module_name = file.stem
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Instancie automatiquement toutes les classes héritant de Rule
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Rule) and attr is not Rule:
                    instance = attr()
                    list_rules.append(instance)
                    instance.on_add()  # si tu veux déclencher on_add automatiquement

def get_random_rule():
    """Retourne une règle aléatoire"""
    if not list_rules:
        raise Exception("Aucune règle chargée. Appelle load_rules() d'abord.")
    return random.choice(list_rules)

def run_rule(rule):
    """Exécute une règle"""
    print(f"Exécution de la règle : {rule._name}")
    print(f"Description : {rule._description}")
if __name__ == "__main__":
    load_rules()  # charge toutes les règles

    print("Toutes les règles chargées :")
    for r in list_rules:
        print("-", r._name)

    print("\nRègle aléatoire test :")
    rule = get_random_rule()
    run_rule(rule)
