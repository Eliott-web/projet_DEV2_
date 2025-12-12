import random
from main.rules.rule import Rule
from main.rules.rules_def.scorex2 import ScoreX2
from main.rules.rules_def.turbo_tchikita import Turbo

list_rules = []
list_available_rules = [ScoreX2(), Turbo()]

def add_rule(rule: Rule):
    """Ajoute une règle à la liste active et la retire des règles disponibles"""
    if rule in list_available_rules:
        list_available_rules.remove(rule)
    list_rules.append(rule)
    rule.on_add()

def remove_rule(rule: Rule):
    """Retire une règle de la liste active et la remet dans les règles disponibles"""
    if rule in list_rules:
        list_rules.remove(rule)
        rule.on_remove()
        if rule not in list_available_rules:
            list_available_rules.append(rule)

def get_random_rule() -> Rule:
    """Retourne une règle aléatoire parmi celles disponibles"""
    if not list_available_rules:
        return None
    return random.choice(list_available_rules)

def get_random_active_rule() -> Rule:
    """Retourne une règle aléatoire parmi celles actives"""
    if not list_rules:
        return None
    return random.choice(list_rules)

def add_random_rule():
    """Ajoute une règle aléatoire depuis les règles disponibles"""
    rule = get_random_rule()
    if rule:
        add_rule(rule)

def remove_random_rule():
    """Retire une règle aléatoire depuis les règles actives"""
    rule = get_random_active_rule()
    if rule:
        remove_rule(rule)

def random_rule_event():
    """Événement aléatoire qui ajoute ou retire une règle
    - Si aucune règle disponible, force la suppression d'une règle active
    - Si aucune règle active, force l'ajout d'une règle disponible
    - Sinon, choix aléatoire entre ajouter ou retirer
    
    Returns:
        tuple: (Rule, bool) - La règle affectée et True si ajoutée, False si retirée
               ou (None, None) si aucune action n'a pu être effectuée
    """
    # Si aucune règle disponible, on doit obligatoirement retirer
    if not list_available_rules and list_rules:
        rule = get_random_active_rule()
        if rule:
            remove_rule(rule)
            return (rule, False)
    # Si aucune règle active, on doit obligatoirement ajouter
    elif not list_rules and list_available_rules:
        rule = get_random_rule()
        if rule:
            add_rule(rule)
            return (rule, True)
    # Sinon, choix aléatoire
    elif list_available_rules and list_rules:
        if random.choice([True, False]):
            rule = get_random_rule()
            if rule:
                add_rule(rule)
                return (rule, True)
        else:
            rule = get_random_active_rule()
            if rule:
                remove_rule(rule)
                return (rule, False)
    
    return (None, None)