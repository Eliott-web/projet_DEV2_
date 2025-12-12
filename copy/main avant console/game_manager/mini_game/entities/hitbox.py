# ...existing code...

class Hitbox:
    def __init__(self,source, hitbox_size=(0,0), position=(0,0)):
        self._image = None
        self._hitbox_size = hitbox_size
        self._position = position
        self._source = source
        # register in manager
        from .hitbox_manager import HitboxManager
        HitboxManager.instance().register(self)

    def get_source(self):
        return self._source
    
    def get_image(self):
        return self._image

    def get_position(self):
        return self._position
    
    def set_image(self, image):
        image.set_position(self.get_position())
        self._image = image

    def set_position(self, x, y):
        self._position = (x, y)
        image = self.get_image()
        if self.has_image():
            image.set_position((x, y))

    def has_image(self):
        return self._image is not None

    def get_hitbox_size(self):
        return self._hitbox_size

    def get_bounds(self):
        """Return (x0,y0,x1,y1) using center-position convention."""
        x, y = self.get_position()
        w, h = self.get_hitbox_size()
        half_w, half_h = w / 2.0, h / 2.0
        return (x - half_w, y - half_h, x + half_w, y + half_h)
    
    def kill(self):
        # Clean up resources, unregister from hitbox manager, etc.
        from .hitbox_manager import HitboxManager
        HitboxManager.instance().unregister(self)
        
        self.get_image().kill()
        del self

    @staticmethod
    def _aabb_intersect(a, b, margin: float = 0.0) -> bool:
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        return not (ax1 + margin < bx0 or ax0 - margin > bx1 or ay1 + margin < by0 or ay0 - margin > by1)

    def intersects(self, other, margin: float = 0.0) -> bool:
        """Collision test against another hitbox."""
        return self._aabb_intersect(self.get_bounds(), other.get_bounds(), margin)

    def nearby(self, margin: float = 0.0):
        """Return hitboxes currently overlapping this one (via manager)."""
        from .hitbox_manager import HitboxManager
        return HitboxManager.instance().query_overlaps(self, margin)

    def __del__(self):
        # unregister on destruction
        try:
            from .hitbox_manager import HitboxManager
            HitboxManager.instance().unregister(self)
        except (ImportError, AttributeError):
            # Python is shutting down, ignore the error
            pass
# ...existing code...