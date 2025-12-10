# wall.py
from ..hitbox import Hitbox

class Wall(Hitbox):
    def __init__(self, position, hitbox_size):
        # Same pattern as Ground
        super().__init__(self, hitbox_size, position=position)
        self._is_wall = True
        
    def is_wall(self):
        return True