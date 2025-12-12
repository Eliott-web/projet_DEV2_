from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mob import Mob


class PionEntity(Mob):

    def __init__(self, position):
        from main.gui.widget.image import ImageWidget
        name = "Pion"
        vitesse = 10
        size = 128
        hitbox_size = (size, size)
        gravity = 0.0
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        
        sprite = ImageWidget("assets/mobs/pion.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        self._apply_forces  = False