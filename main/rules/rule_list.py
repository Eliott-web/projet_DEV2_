import os
import importlib.util
from pathlib import Path
import random

list_rules = []

def add_rule(rule):
    """Ajoute une règle à la liste et appelle on_add"""
    list_rules.append(rule)
    rule.on_add()

def load_rules():
    """
    Importe automatiquement tous les fichiers Python du dossier rules_def.
    Chaque fichier doit contenir une classe qui hérite de Rule et qui s'instancie elle-même
    en appelant add_rule() à la fin du fichier.
    """
    RULES_DIR = Path(__file__).parent / "rules_def"

    for file in RULES_DIR.iterdir():
        if file.suffix == ".py" and not file.name.startswith("__"):
            module_name = file.stem
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    print("Règles chargées :", [r._name for r in list_rules])

def get_random_rule():
    """Retourne une règle aléatoire"""
    if not list_rules:
        raise Exception("Aucune règle chargée. Appelle load_rules() d'abord.")
    return random.choice(list_rules)

def run_rule(rule):
    """Exécute une règle (ici on affiche juste le nom et description)"""
    print(f"Exécution de la règle : {rule._name}")
    print(f"Description : {rule._description}")
    # L'effet réel se produit via on_add() déjà appelé lors de add_rule()

# Exemple d'utilisation
if __name__ == "__main__":
    load_rules()

    # Sélection aléatoire et exécution
    rule = get_random_rule()
    run_rule(rule)
