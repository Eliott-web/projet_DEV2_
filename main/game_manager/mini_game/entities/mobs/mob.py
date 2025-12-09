from main.gui.fenetre import HEIGHT, WIDTH
from ..hitbox import Hitbox
from ..objets.wall import Wall

class Mob(Hitbox):
# In mob.py
    def __init__(self, name, vitesse, position, hitbox_size=(50, 50)):  # Add position parameter
        super().__init__(self, position, hitbox_size)
        self._name = name
        self._vitesse = vitesse
        self._position = position
        self._destination = None
        self._position0 = position
        
    def get_position0(self):
        return self._position0

    def set_position0(self, x, y):
        self._position0 = (x, y)

    def loop(self):
        self.refresh_position()
        self.image_animation_loop()

        self.set_position0(*self.get_position())

    def get_name(self):
        return self._name

    def get_vitesse(self):
        return self._vitesse
    
    def set_position(self, x, y):
        self._position = (x, y)
        super().set_position(x, y)
    
    def set_destination_relative(self, dx, dy):
        dest_x = self._position[0] + dx
        dest_y = self._position[1] + dy
        self._destination = (dest_x, dest_y)

    def set_destination(self, x, y):
        self._destination = (x, y)
    
    def stop(self):
        self._destination = None

    def kill(self):
        # Clean up resources, unregister from hitbox manager, etc.
        self.get_image().kill()
        del self

    #Hitbox Section

    def is_colliding(self):
        colliding = self.get_colliding_hitboxes()
        if len(colliding) > 0:
            return True
        return False
    
    def get_colliding_hitboxes(self):
        colliding = []
        nearby_hitboxes = self.nearby()
        for hb in nearby_hitboxes:
            if hb.get_source() != self:
                colliding.append(hb)
        return colliding
    
    def is_colliding_with_walls(self):
        colliding = self.get_colliding_hitboxes()
        for hb in colliding:
            if isinstance(hb.get_source(), Wall):
                return True
        return False
    
    def image_animation_loop(self):
        image = self.get_image()
        if image is None:
                return
        
        from main.game_manager.mini_game.mini_game import MiniGame
        x = self.get_position()[0]
        y = self.get_position()[1]
        x0 = self.get_position0()[0]
        y0 = self.get_position0()[1]
        speed = self.get_vitesse()

        if (y != y0):
            dt = 1 / MiniGame.refresh_rate  # Assuming a fixed time step for simplicity
            x += speed * dt
            y += speed * dt
        
        dx = x - x0
        dy = y - y0

        image.set_movement_tilt(dx , dy)



    # Position and movement methods
    def refresh_position(self):

        if self._destination is None:
            return
        
        print(f"{self._name} position: {self._position}")
        
        x0, y0 = self._position
        dest_x, dest_y = self._destination
        
        x = self.axis_move(x0, dest_x)
        y = self.axis_move(y0, dest_y)
        self.set_position(x, y)

        if (x, y) == self._destination:
            self.stop()
        
    def axis_move(self, axis, axis_dest):
        if axis < axis_dest:
            axis += self._vitesse
            if axis > axis_dest:
                axis = axis_dest
        elif axis > axis_dest:
            axis -= self._vitesse
            if axis < axis_dest:
                axis = axis_dest
        return axis