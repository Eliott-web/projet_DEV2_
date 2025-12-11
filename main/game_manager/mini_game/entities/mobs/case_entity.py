from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mob import Mob
from main.gui.widget.image import ImageWidget


class CaseEntity(Mob):

    def __init__(self, position):
        name = "Case"
        vitesse = 10
        size = 265
        hitbox_size = (size, size)
        gravity = 0.0
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        
        sprite = ImageWidget("assets/mobs/mario.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        self._apply_forces  = False