from main.gui.fenetre import HEIGHT, WIDTH
from ..hitbox import Hitbox
from ..objets.wall import Wall

class Mob(Hitbox):
    def __init__(self, name, vitesse, position, hitbox_size=(50, 50), gravity=0.5):
        super().__init__(self, position, hitbox_size)
        self._name = name
        self._vitesse = vitesse  # Base movement speed
        self._position = position
        self._destination = None
        self._position0 = position
        
        # Physics properties
        self._velocity = [0.0, 0.0]  # [vx, vy]
        self._acceleration = [0.0, 0.0]  # [ax, ay]
        self._gravity = gravity  # Default gravity strength
        self._gravity_enabled = True
        self._mass = 1.0  # Mass affects how forces apply
        self._friction = 0.9  # Ground friction (0.0 to 1.0)
        self._air_resistance = 0.98  # Air resistance (0.0 to 1.0)
        self._max_fall_speed = 15.0  # Terminal velocity
        self._is_grounded = False
        self._jump_power = 12.0  # Jump strength
        self._apply_forces = True  # Enable/disable physics
        
    # Existing methods remain...
    def get_position0(self):
        return self._position0

    def set_position0(self, x, y):
        self._position0 = (x, y)

    def loop(self):
        if self._apply_forces:
            self.apply_physics()
        else:
            self.refresh_position()  # Original movement system
        
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
        self._velocity = [0.0, 0.0]  # Also stop physics movement

    def kill(self):
        self.get_image().kill()
        del self

    # PHYSICS METHODS
    def apply_physics(self):
        """Apply physics calculations including gravity and movement"""
        # Apply gravity if enabled
        if self._gravity_enabled and not self._is_grounded:
            self._acceleration[1] += self._gravity
        
        # Update velocity with acceleration
        self._velocity[0] += self._acceleration[0]
        self._velocity[1] += self._acceleration[1]
        
        # Apply air resistance when not grounded
        if not self._is_grounded:
            self._velocity[0] *= self._air_resistance
            self._velocity[1] *= self._air_resistance
        
        # Apply friction when grounded
        if self._is_grounded:
            self._velocity[0] *= self._friction
        
        # Limit fall speed (terminal velocity)
        if self._velocity[1] > self._max_fall_speed:
            self._velocity[1] = self._max_fall_speed
        
        # Calculate new position
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        
        # Check for collisions before moving
        old_position = self._position
        self.set_position(new_x, new_y)
        
        # Handle wall collisions
        if self.is_colliding_with_walls():
            # Restore old position
            self.set_position(*old_position)
            
            # Bounce or stop based on collision
            colliding = self.get_colliding_hitboxes()
            for hb in colliding:
                if isinstance(hb.get_source(), Wall):
                    # Simple collision response - reverse velocity
                    self._velocity[0] *= -0.5  # Bounce with energy loss
                    self._velocity[1] *= -0.5
                    
                    # Check if we're on ground (collision from top)
                    if old_position[1] < self._position[1]:
                        self._is_grounded = True
                        self._velocity[1] = 0  # Stop vertical movement
                    break
        
        # Reset acceleration for next frame
        self._acceleration = [0.0, 0.0]
        
        # Reset grounded status (will be set again if collision occurs)
        self._is_grounded = False

    def apply_force(self, fx, fy):
        """Apply a force to the mob (force = mass * acceleration)"""
        ax = fx / self._mass
        ay = fy / self._mass
        self._acceleration[0] += ax
        self._acceleration[1] += ay

    def set_velocity(self, vx, vy):
        """Set the mob's velocity directly"""
        self._velocity = [vx, vy]

    def jump(self, power=None):
        """Make the mob jump"""
        if not self._is_grounded:
            return False  # Can't jump in air (optional: allow double jump)
        
        jump_strength = power if power is not None else self._jump_power
        self._velocity[1] = -jump_strength  # Negative Y is up
        self._is_grounded = False
        return True

    # GRAVITY CONTROL METHODS
    def set_gravity(self, gravity_strength):
        """Set the gravity strength for this mob"""
        self._gravity = gravity_strength
    
    def get_gravity(self):
        """Get the current gravity strength"""
        return self._gravity
    
    def enable_gravity(self):
        """Enable gravity for this mob"""
        self._gravity_enabled = True
    
    def disable_gravity(self):
        """Disable gravity for this mob"""
        self._gravity_enabled = False
        self._velocity[1] = 0  # Stop vertical movement
    
    def set_mass(self, mass):
        """Set the mob's mass (affects force application)"""
        if mass > 0:
            self._mass = mass
    
    def set_friction(self, friction):
        """Set ground friction coefficient (0.0 to 1.0)"""
        self._friction = max(0.0, min(1.0, friction))
    
    def set_air_resistance(self, resistance):
        """Set air resistance coefficient (0.0 to 1.0)"""
        self._air_resistance = max(0.0, min(1.0, resistance))
    
    def set_max_fall_speed(self, speed):
        """Set terminal velocity for falling"""
        self._max_fall_speed = speed
    
    def set_jump_power(self, power):
        """Set jump strength"""
        self._jump_power = power
    
    def is_grounded(self):
        """Check if mob is on the ground"""
        return self._is_grounded
    
    def enable_physics(self):
        """Enable physics system"""
        self._apply_forces = True
    
    def disable_physics(self):
        """Disable physics system (use original movement)"""
        self._apply_forces = False
        self._velocity = [0.0, 0.0]
        self._acceleration = [0.0, 0.0]

    # EXISTING METHODS (updated for physics)
    def image_animation_loop(self):
        image = self.get_image()
        if image is None:
            return
        
        from main.game_manager.mini_game.mini_game import MiniGame
        x = self.get_position()[0]
        y = self.get_position()[1]
        x0 = self.get_position0()[0]
        y0 = self.get_position0()[1]
        
        dx = x - x0
        dy = y - y0
        
        # Use velocity for animation if physics is enabled
        if self._apply_forces:
            dx = self._velocity[0]
            dy = self._velocity[1]
        
        image.set_movement_tilt(dx, dy)

    # Hitbox methods remain the same...
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