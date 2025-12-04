from ..hitbox import Hitbox
from ..objets.wall import Wall

class Mob(Hitbox):
    def __init__(self, name, vitesse, hitbox_size):
        position = (0,0)
        super().__init__(hitbox_size, position, source=self)
        self._name = name
        self._vitesse = vitesse
        self._position = position
        self._destination = None
        
        
    def loop(self):
        self.refresh_position()

    def get_name(self):
        return self._name

    def get_vitesse(self):
        return self._vitesse
    
    def set_position(self, x, y):
        self._position = (x, y)
    
    def set_destination(self, x, y):
        self._destination = (x, y)
    
    def stop(self):
        self._destination = None

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