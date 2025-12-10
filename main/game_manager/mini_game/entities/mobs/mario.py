from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mob import Mob
from main.gui.widget.image import ImageWidget


class Mario(Mob):
    motion_speed = 50  # Vitesse de déplacement horizontale

    def __init__(self, position):
        name = "Mario"
        vitesse = 20
        size = 128
        hitbox_size = (size, size)
        gravity = 2.0
        self._is_touching_koopa = False
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        self.enable_physics()
        
        sprite = ImageWidget("assets/mobs/mario.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        
        # Initialize with zero velocity
        self.set_velocity(0, 0)
        self.set_max_fall_speed(80)  # Limit falling speed

    def jump(self):
        if self.is_grounded():
            self.apply_force(0, -31)  # Apply an upward force to jump

    def loop(self):
        if self.is_colliding():
            self.on_collision()
        super().loop()

    def on_collision(self):
        # Gérer la collision avec d'autres entités si nécessaire
        collections = self.get_colliding_hitboxes()
        for entity in collections:
            if isinstance(entity, Koopa):
                self.touched_koopa()

    def set_touching_koopa(self, touched: bool):
        self._is_touching_koopa = touched

    def has_touched_koopa(self):
        return self._is_touching_koopa

    def touched_koopa(self):
       self.set_touching_koopa(True)