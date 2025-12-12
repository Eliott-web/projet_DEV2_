from typing import Iterable, List, Tuple

class HitboxManager:
    _instance = None

    def __init__(self):
        self._hitboxes = set()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = HitboxManager()
        return cls._instance

    def register(self, hb):
        self._hitboxes.add(hb)

    def unregister(self, hb):
        self._hitboxes.discard(hb)

    def _get_bounds(self, hb) -> Tuple[float, float, float, float]:
        
        """
        Return (x0, y0, x1, y1) - assumes hitbox provides either:
         - hb.get_bounds() -> (x0,y0,x1,y1)
         - or hb.get_position() -> (x,y) and hb.get_hitbox_size() -> (w,h)
         - or attributes _position and _hitbox_size
        Position is treated as center.
        """
        if hasattr(hb, "get_bounds"):
            return hb.get_bounds()
        if hasattr(hb, "get_position") and hasattr(hb, "get_hitbox_size"):
            x, y = hb.get_position()
            w, h = hb.get_hitbox_size()
        else:
            # fallback on common attribute names
            x, y = getattr(hb, "_position", (0, 0))
            w, h = getattr(hb, "_hitbox_size", getattr(hb, "hitbox_size", (0, 0)))
        half_w, half_h = w / 2.0, h / 2.0
        return (x - half_w, y - half_h, x + half_w, y + half_h)

    @staticmethod
    def _aabb_intersect(a: Tuple[float,float,float,float], b: Tuple[float,float,float,float], margin: float = 0.0) -> bool:
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        return not (ax1 + margin < bx0 or ax0 - margin > bx1 or ay1 + margin < by0 or ay0 - margin > by1)

    def query_overlaps(self, target, margin: float = 0.0) -> List:
        """
        Retourne la liste des hitboxes (sauf target) qui intersectent target.
        margin : agrandit/shrink l'AABB pour tolérance.
        """
        target_bounds = self._get_bounds(target)
        result = []
        for hb in self._hitboxes:
            if hb is target:
                continue
            try:
                if self._aabb_intersect(target_bounds, self._get_bounds(hb), margin):
                    result.append(hb)
            except Exception:
                # ignore hitboxes that ne respectent pas l'interface
                continue
        return result