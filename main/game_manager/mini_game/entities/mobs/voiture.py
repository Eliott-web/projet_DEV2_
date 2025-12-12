from main.gui.widget.image import ImageWidget
from .mob import Mob

from main.game_manager.mini_game.entities.objets.parking import Parking


class Car(Mob):
    motion_speed = 50  # Vitesse de déplacement horizontale

    def __init__(self, position):
        name = "Car"
        vitesse = 20
        size = 128*1.5
        hitbox_size = (size, size*0.7)
        gravity = 0
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        self.enable_physics()
        
        sprite = ImageWidget("assets/mobs/car.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        
        # Initialize with zero velocity
        self.set_velocity(0, 0)
        self.set_max_fall_speed(80)  # Limit falling speed
        self._air_resistance = 0.9
        self.is_parking = False


    def loop(self):
        if self.is_colliding():
            self.on_collision()
        super().loop()

    def on_collision(self):
        # Gérer la collision avec d'autres entités si nécessaire
        collections = self.get_colliding_hitboxes()
        for entity in collections:
            if isinstance(entity, Parking):
                self.touche_parking()

    def touche_parking(self):
        self.is_parking = True

    def get_has_touche_parking(self):
        return self.is_parking