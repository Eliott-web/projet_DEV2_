from main.game_manager.mini_game.entities.mobs.mob import Mob


class Koopa(Mob):
    motion_speed = 50  # Vitesse de déplacement horizontale

    def __init__(self, position):
        from main.gui.widget.image import ImageWidget
        name = "Koopa"
        vitesse = 20
        size = 128
        hitbox_size = (size, size)
        gravity = 0.5
        self.sensInverse = False  # Pour gérer le sens de déplacement
        super().__init__(name, vitesse, position, hitbox_size, gravity)
        
        # IMPORTANT: Enable physics BEFORE setting image
        self.enable_physics()
        
        sprite = ImageWidget("assets/mobs/koopa.png", position, hitbox_size, 
            anchor="center", on_click=lambda w: None)
        self.set_image(sprite)
        
        # Initialize with zero velocity
        self.set_velocity(0, 0)
        self.set_max_fall_speed(80)  # Limit falling speed

    def loop(self):
        self.movement_logic()
        super().loop()

    def movement_logic(self):
        speed = Koopa.motion_speed
        if self.sensInverse:
            speed = -speed
        
        # Direct velocity control (no acceleration)
        self._velocity[0] = speed
    
    def get_sens_inverse(self):
        return self.sensInverse
    
    def set_sens_inverse(self, sens):
        self.sensInverse = sens

    def on_y_edge(self):
        self.set_sens_inverse(not self.get_sens_inverse())
        
