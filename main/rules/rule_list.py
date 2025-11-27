from rules_def.scorex2 import score2x

list_rules = []

def add_rule(rule):
    list_rules.append(rule)
    rule.on_add()

add_rule(score2x())