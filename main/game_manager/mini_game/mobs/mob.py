class Mob:
    def __init__(self, name, vitesse, hitbox_size):
        self._name = name
        self._vitesse = vitesse
        self._position = (0, 0)
        self._destination = None
        self._hitbox_size = hitbox_size
        
        
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

    # Hitbox methods
    def get_hitbox(self):
        x, y = self._position
        size = self._hitbox_size
        return (x - size / 2, y - size / 2, x + size / 2, y + size / 2)
    
    def is_colliding_with(self, other_mob):
        x1_min, y1_min, x1_max, y1_max = self.get_hitbox()
        x2_min, y2_min, x2_max, y2_max = other_mob.get_hitbox()

        return not (x1_max < x2_min or x1_min > x2_max or y1_max < y2_min or y1_min > y2_max)
    
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