from main.item.item import Item


class RedBull(Item):
    def __init__(self):
        super().__init__(
            name="Red Bull",
            description="Vous fait avancer d'une case supplémentaire lors de votre prochain déplacement.",
            image_path="assets/items/redbull.png"
        )

    def onUse(self):
        import main.main_loop.plateau_menu as plateau_menu
        plateau_menu.case_bonus += 1
        print(f"Red Bull utilisé ! case_bonus = {plateau_menu.case_bonus}")