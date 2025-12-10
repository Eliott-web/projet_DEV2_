# ground.py
from ..hitbox import Hitbox

class Ground(Hitbox):
    def __init__(self, position, hitbox_size):
        # Pass hitbox_size as first argument, then position
        super().__init__(self,hitbox_size, position=position)
        self._is_ground = True
        
    def is_ground(self):
        return True