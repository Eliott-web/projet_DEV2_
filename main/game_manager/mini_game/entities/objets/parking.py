# ground.py
from ..hitbox import Hitbox
from main.gui.widget.image import ImageWidget

class Parking(Hitbox):
    def __init__(self, position):
        # Pass hitbox_size as first argument, then position
        hitbox_size = (100, 100)
        super().__init__(self,hitbox_size, position=position)
        sprite = ImageWidget("assets/mobs/mario.png", position, hitbox_size,
                             anchor="center", on_click=lambda w: None)
        self.set_image(sprite)