from main.game_manager.mini_game.entities.mobs.mob import Mob
from main.gui.widget.image import ImageWidget


class Koopa(Mob):
    def __init__(self,position):
        name = "Koopa"
        vitesse = 20
        size = 128
        hitbox_size = (size, size)
        super().__init__(name, vitesse, position, hitbox_size)

        sprite = ImageWidget("assets/mobs/koopa.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)