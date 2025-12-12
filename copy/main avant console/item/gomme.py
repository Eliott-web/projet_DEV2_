from main.item.item import Item


class Gomme(Item):
    def __init__(self):
        super().__init__(
            name="Gomme",
            description="Retire une règle aléatoirement du jeu.",
            image_path="assets/items/gomme.png"
        )

    def onUse(self):
        from main.rules.rule_list import get_random_active_rule, remove_rule
        from main.main_loop.plateau_menu import PlateauMenu
        
        # Récupérer une règle active aléatoire
        rule = get_random_active_rule()
        
        if rule:
            # Retirer la règle
            remove_rule(rule)
            print(f"Gomme utilisée : règle '{rule.name}' retirée !")
            
            # Afficher la règle retirée (nécessite l'accès au menu)
            # On suppose que le menu est accessible via un gestionnaire global
            # Sinon, on peut juste print
        else:
            print("Aucune règle active à retirer !")