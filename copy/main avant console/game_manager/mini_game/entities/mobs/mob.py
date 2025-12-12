from main.gui.fenetre import HEIGHT, WIDTH
from ..hitbox import Hitbox
from ..objets.wall import Wall
from ..objets.ground import Ground  # Import the new Ground class

class Mob(Hitbox):
    def __init__(self, name, vitesse, position, hitbox_size=(50, 50), gravity=0.5):
        # Fix: The first argument to super().__init__() should not be 'self'
        super().__init__(position, hitbox_size)
        self._name = name
        self._vitesse = vitesse
        self._position = position
        self._destination = None
        self._position0 = position
        
        # Physics properties
        self._velocity = [0.0, 0.0]
        self._acceleration = [0.0, 0.0]
        self._gravity = gravity
        self._gravity_enabled = True
        self._mass = 1.0
        self._friction = 0.9
        self._air_resistance = 0.98
        self._max_fall_speed = 15.0
        self._is_grounded = False
        self._jump_power = 12.0
        self._apply_forces = True
        
        # Ground detection
        self._ground_check_offset = 5  # How far below to check for ground
        self._ground_normal = [0, -1]  # Normal vector of ground (points up)
        self._slope_limit = 0.7  # Maximum slope the mob can walk on
        
    # EXISTING METHODS FROM ORIGINAL CLASS
    def get_position0(self):
        return self._position0

    def set_position0(self, x, y):
        self._position0 = (x, y)

    def get_name(self):
        return self._name

    def get_vitesse(self):
        return self._vitesse
    
    def get_hitbox_size(self):
        return super().get_hitbox_size()
    
    def get_position(self):
        return self._position
    
    def set_vitesse(self, vitesse):
        self._vitesse = vitesse

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
        super().kill()

    # ORIGINAL MOVEMENT METHODS
    def refresh_position(self):
        if self._destination is None:
            return
        
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

    def loop(self):
        if self._apply_forces:
            self.apply_physics()
            self.check_ground_collision()  # Check for ground continuously
        else:
            self.refresh_position()
        
        self.image_animation_loop()
        self.set_position0(*self.get_position())
        self.check_edges()

    # PHYSICS METHODS
    def apply_physics(self):
        """Apply physics calculations including gravity and movement"""
        # Apply gravity if enabled and not grounded
        if self._gravity_enabled and not self._is_grounded:
            self._acceleration[1] += self._gravity
        
        # Update velocity with acceleration
        self._velocity[0] += self._acceleration[0]
        self._velocity[1] += self._acceleration[1]
        
        # Apply air resistance when not grounded
        if not self._is_grounded:
            self._velocity[0] *= self._air_resistance
            self._velocity[1] *= self._air_resistance
        else:
            # Apply friction when grounded
            self._velocity[0] *= self._friction
        
        # Limit fall speed (terminal velocity)
        if self._velocity[1] > self._max_fall_speed:
            self._velocity[1] = self._max_fall_speed
        
        # Calculate new position
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        
        # Store old position for collision detection
        old_position = self._position
        self.set_position(new_x, new_y)
        
        # Check for collisions
        if self.is_colliding():
            self.handle_collision(old_position)
        
        # Reset acceleration for next frame
        self._acceleration = [0.0, 0.0]
        
        # Reset grounded status (will be updated in check_ground_collision)
        if not self._is_grounded or abs(self._velocity[1]) > 0.1:
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
        """Make the mob jump - requires being on ground"""
        if not self._is_grounded:
            return False
        
        jump_strength = power if power is not None else self._jump_power
        self._velocity[1] = -jump_strength
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

    # GROUND COLLISION METHODS
    def check_ground_collision(self):
        """Check if the mob is standing on ground"""
        # Only check if we're falling or standing
        if self._velocity[1] >= 0:  # Falling or stationary
            # Create a small hitbox below the mob to check for ground
            feet_position = (self._position[0], self._position[1] + self.get_hitbox_size()[1]/2 + self._ground_check_offset)
            feet_size = (self.get_hitbox_size()[0], self._ground_check_offset * 2)
            
            # Temporarily create a hitbox to check for collisions
            temp_hitbox = Hitbox(feet_position, feet_size)
            nearby = temp_hitbox.nearby()
            
            for hb in nearby:
                source = hb.get_source()
                # Check if it's ground
                if hasattr(source, '_is_ground') and source._is_ground:
                    # Check if we're actually above the ground
                    mob_bottom = self._position[1] + self.get_hitbox_size()[1]/2
                    ground_top = hb.get_position()[1] - hb.get_hitbox_size()[1]/2
                    
                    if mob_bottom <= ground_top + self._ground_check_offset:
                        self._is_grounded = True
                        # Snap to ground surface
                        if self._velocity[1] > 0:  # Only snap if falling
                            new_y = ground_top - self.get_hitbox_size()[1]/2
                            self.set_position(self._position[0], new_y)
                            self._velocity[1] = 0
                        return True
        return False

    def handle_collision(self, old_position):
        """Handle collisions with walls and ground"""
        colliding = self.get_colliding_hitboxes()
        
        for hb in colliding:
            source = hb.get_source()
            
            # Handle Ground collisions
            if hasattr(source, '_is_ground') and source._is_ground:
                self.handle_ground_collision(hb, old_position)
            
            # Handle Wall collisions
            elif hasattr(source, '_is_wall') and source._is_wall:
                self.handle_wall_collision(hb, old_position)
            
            # Handle other Mob collisions
            elif isinstance(source, Mob):
                self.handle_mob_collision(hb, old_position)

    def handle_ground_collision(self, ground_hitbox, old_position):
        """Handle collision with ground"""
        mob_left = self._position[0] - self.get_hitbox_size()[0]/2
        mob_right = self._position[0] + self.get_hitbox_size()[0]/2
        mob_top = self._position[1] - self.get_hitbox_size()[1]/2
        mob_bottom = self._position[1] + self.get_hitbox_size()[1]/2
        
        ground_left = ground_hitbox.get_position()[0] - ground_hitbox.get_hitbox_size()[0]/2
        ground_right = ground_hitbox.get_position()[0] + ground_hitbox.get_hitbox_size()[0]/2
        ground_top = ground_hitbox.get_position()[1] - ground_hitbox.get_hitbox_size()[1]/2
        ground_bottom = ground_hitbox.get_position()[1] + ground_hitbox.get_hitbox_size()[1]/2
        
        # Determine collision side
        overlap_left = mob_right - ground_left
        overlap_right = ground_right - mob_left
        overlap_top = mob_bottom - ground_top
        overlap_bottom = ground_bottom - mob_top
        
        # Find minimum overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
        
        if min_overlap == overlap_top:  # Hitting ground from above
            # Snap to ground surface
            self.set_position(self._position[0], ground_top - self.get_hitbox_size()[1]/2)
            self._is_grounded = True
            self._velocity[1] = 0  # Stop falling
            
        elif min_overlap == overlap_bottom:  # Hitting ground from below
            self.set_position(self._position[0], ground_bottom + self.get_hitbox_size()[1]/2)
            self._velocity[1] = 0  # Stop upward movement
            
        elif min_overlap == overlap_left:  # Hitting ground from left
            self.set_position(ground_left - self.get_hitbox_size()[0]/2, self._position[1])
            self._velocity[0] = 0  # Stop horizontal movement
            
        elif min_overlap == overlap_right:  # Hitting ground from right
            self.set_position(ground_right + self.get_hitbox_size()[0]/2, self._position[1])
            self._velocity[0] = 0  # Stop horizontal movement

    def handle_wall_collision(self, wall_hitbox, old_position):
        """Handle collision with walls"""
        # Restore old position
        self.set_position(*old_position)
        
        # Simple bounce with energy loss
        self._velocity[0] *= -0.3
        self._velocity[1] *= -0.3

    def handle_mob_collision(self, mob_hitbox, old_position):
        """Handle collision with other mobs"""
        # Optional: add mob-to-mob collision response
        pass

    def move(self, dx, dy):
        """Move the mob with ground awareness"""
        if self._apply_forces:
            # Apply horizontal force for physics-based movement
            self.apply_force(dx * self._mass, 0)
        else:
            # Original movement system
            if dx != 0 or dy != 0:
                new_x = self._position[0] + dx * self._vitesse
                new_y = self._position[1] + dy * self._vitesse
                self.set_position(new_x, new_y)

    # GROUND INTERACTION METHODS
    def get_ground_normal(self):
        """Get the normal vector of the ground we're standing on"""
        return self._ground_normal.copy()
    
    def set_ground_check_offset(self, offset):
        """Set how far below to check for ground"""
        self._ground_check_offset = offset
    
    def can_walk_on_slope(self, slope_x):
        """Check if mob can walk on a given slope"""
        return abs(slope_x) <= self._slope_limit
    
    def set_slope_limit(self, limit):
        """Set maximum walkable slope (0.0 to 1.0)"""
        self._slope_limit = max(0.0, min(1.0, limit))

    # HITBOX METHODS
    def is_colliding(self):
        colliding = self.get_colliding_hitboxes()
        if len(colliding) > 0:
            return True
        return False
    
    def get_colliding_hitboxes(self):
        colliding = []
        nearby_hitboxes = self.nearby()
        for hb in nearby_hitboxes:
            if hb != self:
                colliding.append(hb)
        return colliding
    
    def is_colliding_with_walls(self):
        """Check if colliding with walls (not ground)"""
        collections = self.get_colliding_hitboxes()
        print(collections)
        for entity in collections:
            if isinstance(entity, Wall):
                return True
        return False
    
    def is_colliding_with_ground(self):
        """Check if colliding with ground"""
        colliding = self.get_colliding_hitboxes()
        for hb in colliding:
            source = hb.get_source()
            if hasattr(source, '_is_ground') and source._is_ground:
                return True
        return False

    # ANIMATION METHOD
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

    # detections de coinsz
    def check_edges(self):
        x, y = self._position
        w, h = self.get_hitbox_size()
        
        left = x - w/2
        right = x + w/2
        top = y - h/2
        bottom = y + h/2
        
        if left <= 0:
            self.on_y_edge()
            # self.play_sound("edge_left")
        
        if right >= WIDTH:
            self.on_y_edge()
            # self.play_sound("edge_right")
        
        if top <= 0:
            self.on_x_edge()
            # self.play_sound("edge_top")
        
        if bottom >= HEIGHT:
            self.on_x_edge()
            # self.play_sound("edge_bottom")

    def on_x_edge(self):
        pass

    def on_y_edge(self):
        pass