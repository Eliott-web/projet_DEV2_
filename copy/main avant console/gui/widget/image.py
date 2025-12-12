# main/gui/widget/image.py
import os
import pygame
from typing import Optional, Callable, Tuple
from main import main

class ImageWidget:
    """
    Widget pour afficher une image Pygame avec position, taille, ancre, rotation.
    Ajoute `handle_event(event)` et `on_click` callback pour intégration au WidgetManager.
    """
    def __init__(
        self,
        source,
        pos: Tuple[int,int] = (0,0),
        size: Optional[Tuple[int,int]] = None,
        anchor: str = "topleft",
        rotation: float = 0,
        alpha: int = 255,
        on_click: Optional[Callable] = None
    ):
        self._anchor = anchor
        self._pos = tuple(pos)
        self._rotation = rotation
        self._alpha = max(0, min(255, int(alpha)))
        self._visible = True
        self._original: Optional[pygame.Surface] = None
        self._cached: Optional[pygame.Surface] = None
        self._cached_size = None
        self._on_click = on_click
        self._mouse_down_inside = False
        self._flip_x = False
        self._current_tilt = 0.0  # Track current tilt for smooth transitions

        self.set_image(source)
        if size is not None:
            self.set_size(size)

        manager = main.widget_manager
        manager.add(self)
        manager.bring_to_front(self)
        
        # ⭐⭐ NOUVEAU : ESSAYE DE DESSINER IMMÉDIATEMENT ⭐⭐
        self._try_to_draw_now()
    
    def _try_to_draw_now(self):
        """Essaie de dessiner l'image tout de suite"""
        try:
            import pygame
            # Vérifier si pygame est initialisé
            if pygame.display.get_init():
                # Récupérer l'écran actuel
                screen = pygame.display.get_surface()
                if screen:
                    # Dessiner cette image
                    self.draw(screen)
                    # Rafraîchir l'écran
                    pygame.display.update(self.get_rect())
                    print(f"🖼️ Image affichée immédiatement à {self._pos}")
        except Exception as e:
            # Si ça échoue, c'est pas grave
            pass

    def set_image(self, source):
        was_flipped = getattr(self, '_flip_x', False)
        
        if isinstance(source, pygame.Surface):
            self._original = source.convert_alpha()
        else:
            try:
                self._original = pygame.image.load(str(source)).convert_alpha()
            except Exception:
                w, h = (64, 64)
                surf = pygame.Surface((w, h), pygame.SRCALPHA)
                surf.fill((180, 180, 180, 255))
                pygame.draw.line(surf, (120, 0, 0), (0, 0), (w, h), 3)
                pygame.draw.line(surf, (120, 0, 0), (0, h), (w, 0), 3)
                self._original = surf
        
        # Re-apply flip if needed
        if was_flipped:
            self._original = pygame.transform.flip(self._original, True, False)
            self._flip_x = True
        
        self._invalidate_cache()

    def set_position(self, pos):
        self._pos = tuple(pos)

    def set_size(self, size):
        self._cached_size = tuple(size)
        self._invalidate_cache()

    def set_rotation(self, angle):
        self._rotation = angle % 360
        self._invalidate_cache()

    def set_alpha(self, alpha):
        self._alpha = max(0, min(255, int(alpha)))
        self._invalidate_cache()

    def set_visible(self, visible: bool):
        self._visible = bool(visible)

    def set_on_click(self, callback: Optional[Callable]):
        self._on_click = callback

    def _invalidate_cache(self):
        self._cached = None

    def kill(self):
        manager = main.widget_manager
        manager.remove(self)
        del self

    def _ensure_cached(self):
        if self._original is None:
            return
        size = self._cached_size if self._cached_size is not None else self._original.get_size()
        rot = self._rotation
        if self._cached is None:
            if size != self._original.get_size():
                surf = pygame.transform.smoothscale(self._original, (int(size[0]), int(size[1])))
            else:
                surf = self._original.copy()
            if rot != 0:
                surf = pygame.transform.rotate(surf, rot)
            if self._alpha != 255:
                surf = surf.copy()
                surf.set_alpha(self._alpha)
            self._cached = surf

    def get_rect(self) -> pygame.Rect:
        self._ensure_cached()
        if self._cached is None:
            w, h = (0, 0)
        else:
            w, h = self._cached.get_size()
        rect = pygame.Rect(0, 0, w, h)
        setattr(rect, self._anchor, self._pos)
        return rect

    def draw(self, surface: pygame.Surface):
        if not self._visible:
            return
        self._ensure_cached()
        if self._cached is None:
            return
        rect = self.get_rect()
        surface.blit(self._cached, rect.topleft)

    def point_inside(self, x, y) -> bool:
        return self.get_rect().collidepoint((x, y))

    def handle_event(self, event) -> bool:
        """
        Traitement simplifié des événements :
        - Si un click gauche (MOUSEBUTTONDOWN puis MOUSEBUTTONUP) survient sur le widget,
          appelle `on_click(widget)` si défini. Retourne True si l'événement est consommé.
        """
        import pygame as _pygame
        if event.type == _pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.point_inside(mx, my):
                self._mouse_down_inside = True
                return True  # consommé
            self._mouse_down_inside = False
            return False
        if event.type == _pygame.MOUSEBUTTONUP and event.button == 1:
            mx, my = event.pos
            if self._mouse_down_inside and self.point_inside(mx, my):
                # click completed
                if callable(self._on_click):
                    try:
                        self._on_click(self)
                    except Exception:
                        pass
                self._mouse_down_inside = False
                return True
            self._mouse_down_inside = False
            return False
        return False

    def update(self, dt: float):
        """Optionnel: override or monkeypatch for animation."""
        pass

    def set_movement_tilt(self, dx: float, dy: float, flip_sensitivity: float = 0.1, 
                          tilt_sensitivity: float = 0.5, max_tilt: float = 90.0,
                          tilt_easing: float = 0.3, return_to_neutral_speed: float = 0.5):
        """
        Apply visual effects based on entity movement.
        
        Args:
            dx: Horizontal movement (positive = right, negative = left)
            dy: Vertical movement (positive = falling down, negative = moving up)
            flip_sensitivity: Minimum dx value to trigger flip (avoid jitter)
            tilt_sensitivity: How much tilt per pixel of vertical movement
            max_tilt: Maximum tilt angle in degrees
            tilt_easing: Smooth factor for tilt transitions (0.0-1.0)
            return_to_neutral_speed: How quickly the sprite returns to upright (higher = faster)
        """
        # 1. Handle horizontal flipping (keep flip state as is when dx = 0)
        if abs(dx) > flip_sensitivity:
            # Only flip if there's significant horizontal movement
            if dx > 0 and self._flip_x:  # Moving right but currently flipped left
                self.flip_horizontal(False)
            elif dx < 0 and not self._flip_x:  # Moving left but currently normal
                self.flip_horizontal(True)
        
        # 2. Handle vertical tilting
        if abs(dy) > 0.1:  # Small threshold to prevent micro-movements
            # Negative dy (moving up) = tilt up, Positive dy (falling) = tilt down
            # Apply easing to dy for smoother transitions
            eased_dy = dy * abs(dy) * 0.1  # Quadratic easing for more natural feel
            
            # Calculate target tilt with sensitivity
            target_tilt = -eased_dy * tilt_sensitivity
            
            # Clamp to maximum tilt
            target_tilt = max(-max_tilt, min(max_tilt, target_tilt))
        else:
            # When dy is 0 (or very small), return to neutral rotation
            target_tilt = 0.0
        
        # 3. Apply smooth tilt transition
        # When returning to neutral (target_tilt = 0), use faster easing
        current_easing = return_to_neutral_speed if abs(target_tilt) < 0.1 else tilt_easing
        
        # Smoothly interpolate towards target tilt
        self._current_tilt += (target_tilt - self._current_tilt) * current_easing
        
        # Apply the tilt only if it's significant
        if abs(self._current_tilt) > 0.1:
            self.set_rotation(self._current_tilt)
        elif abs(self._rotation) > 0.1:  # If we have rotation but should be neutral
            self.set_rotation(0)
            self._current_tilt = 0.0  # Reset tracking

    def flip_horizontal(self, flip: bool = True):
        """
        Flip the image horizontally.
        Call this directly if you want manual control.
        """
        if flip != self._flip_x:
            self._flip_x = flip
            if self._original is not None:
                self._original = pygame.transform.flip(self._original, True, False)
                self._invalidate_cache()

    def get_rotation(self) -> float:
        """Get current rotation angle."""
        return self._rotation