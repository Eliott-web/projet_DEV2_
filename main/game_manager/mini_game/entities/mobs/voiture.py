from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mob import Mob
from main.gui.widget.image import ImageWidget


class Car(Mob):
    motion_speed = 50  # Vitesse de déplacement horizontale

    def __init__(self, position):
        name = "Car"
        vitesse = 20
        size = 128
        hitbox_size = (size, size)
        gravity = 0
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        self.enable_physics()
        
        sprite = ImageWidget("assets/mobs/mario.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        
        # Initialize with zero velocity
        self.set_velocity(0, 0)
        self.set_max_fall_speed(80)  # Limit falling speed
        self._air_resistance = 0.7


    def loop(self):
        if self.is_colliding():
            self.on_collision()
        super().loop()

    def on_collision(self):
        if True:
            return
        # Gérer la collision avec d'autres entités si nécessaire
        collections = self.get_colliding_hitboxes()
        for entity in collections:
            if isinstance(entity, Koopa):
                self.touched_koopa()
