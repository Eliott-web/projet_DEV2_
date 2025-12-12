from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mob import Mob


class CaseEntity(Mob):

    def __init__(self, position, isShop: bool = False):
        from main.gui.widget.image import ImageWidget
        name = "Case"
        vitesse = 20
        size = 265
        hitbox_size = (size, size)
        gravity = 0.0
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        
        texture = "assets/mobs/case.png"
        if isShop:
            texture = "assets/mobs/case_shop.png"
        sprite = ImageWidget(texture, position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        self._apply_forces  = False
        self._isShop = isShop

    def isShop(self):
        return self._isShop