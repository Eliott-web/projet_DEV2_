from main.item.item import Item


class RedBull(Item):
    def __init__(self):
        super().__init__(
            name="Red Bull",
            description="Vous fait avancer d'une case supplémentaire lors de votre prochain déplacement.",
            image_path="assets/items/redbull.png"
        )

    def onUse(self):
        from main.main_loop.plateau_menu import case_bonus
        case_bonus += 1