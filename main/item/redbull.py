from main.item.item import Item


class RedBull(Item):
    def __init__(self):
        super().__init__(
            name="Red Bull",
            description="Vous fait avancer d'une case supplémentaire lors de votre prochain déplacement.",
            image_path="assets/items/redbull.png"
        )

    def onUse(self):
        """Utilisation de l'item Red Bull"""
        pass