from ..hitbox import Hitbox
class Wall(Hitbox):
    def __init__(self, hitbox_size):
        super().__init__(hitbox_size, position=(0,0), source=self)
    