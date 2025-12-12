from main.item.item import Item


class Gomme(Item):
    def __init__(self):
        super().__init__(
            name="Gomme",
            description="Retire une règle aléatoirement du jeu.",
            image_path="assets/items/gomme.png"
        )

    def onUse(self):
        pass