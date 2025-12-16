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
        from main.main import isGuiMode
        import main.main as main
        
        # Récupérer une règle active aléatoire
        rule = get_random_active_rule()
        
        if rule:
            # Retirer la règle
            remove_rule(rule)
            
            # Afficher la règle retirée visuellement (seulement en mode GUI)
            if isGuiMode():
                main.mainMenu.displayRemovedRule(rule)
            else:
                # En mode console, afficher dans la console
                print(f"\n🗑️  Gomme utilisée : règle '{rule.name}' retirée !")
                print(f"    {rule.description}")
        else:
            if not isGuiMode():
                print("\n⚠️  Aucune règle active à retirer !")