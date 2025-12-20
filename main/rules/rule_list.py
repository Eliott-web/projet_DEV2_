import random
from main.rules.rule import Rule
from main.rules.rules_def.scorex2 import ScoreX2
from main.rules.rules_def.turbo_tchikita import Turbo
from main.rules.rules_def.mini_jeu_hard import MiniGameRule

class RuleManager:
    def __init__(self):
        self._list_rules = []
        self._list_available_rules = [ScoreX2(), Turbo(), MiniGameRule()]

# ---------- GETTERS ----------
    @property
    def list_rules(self):
        return self._list_rules

    @property
    def list_available_rules(self):
        return self._list_available_rules

    # ---------- SETTERS ----------
    @list_rules.setter
    def list_rules(self, value):
        if isinstance(value, list):
            self._list_rules = value

    @list_available_rules.setter
    def list_available_rules(self, value):
        if isinstance(value, list):
            self._list_available_rules = value


manager = RuleManager()


def add_rule(rule: Rule):
    """Ajoute une règle à la liste active et la retire des règles disponibles"""
    try:
        if rule in manager.list_available_rules:
            manager.list_available_rules.remove(rule)
        manager.list_rules.append(rule)
        rule.on_add()
    except Exception as e:
        print("Erreur lors de l'ajout de la règle :", e)


def remove_rule(rule: Rule):
    """Retire une règle de la liste active et la remet dans les règles disponibles"""
    try:
        if rule in manager.list_rules:
            manager.list_rules.remove(rule)
            rule.on_remove()
            if rule not in manager.list_available_rules:
                manager.list_available_rules.append(rule)
    except Exception as e:
        print("Erreur lors de la suppression de la règle :", e)

def get_random_rule() -> Rule:
    """Retourne une règle aléatoire parmi celles disponibles"""
    if not manager.list_available_rules:
        return None
    return random.choice(manager.list_available_rules)


def get_random_active_rule() -> Rule:
    """Retourne une règle aléatoire parmi celles actives"""
    if not manager.list_rules:
        return None
    return random.choice(manager.list_rules)


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
    """Événement aléatoire qui ajoute ou retire une règle"""
    if not manager.list_available_rules and manager.list_rules:
        rule = get_random_active_rule()
        if rule:
            remove_rule(rule)
            return (rule, False)

    elif not manager.list_rules and manager.list_available_rules:
        rule = get_random_rule()
        if rule:
            add_rule(rule)
            return (rule, True)

    elif manager.list_available_rules and manager.list_rules:
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