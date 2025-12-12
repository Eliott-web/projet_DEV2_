# main/gui/widget/text.py
import pygame
from typing import Optional, Callable, Tuple
from main import main


class TextWidget:
    """
    Widget pour afficher du texte comme une image via Pygame.
    Gère position, taille, rotation, alpha, police, couleur.
    Ajoute `handle_event(event)` et `on_click` callback pour intégration au WidgetManager.
    """
    def __init__(
        self,
        text,
        font_size=32,
        color=(255, 255, 255),
        pos=(0, 0),
        anchor="topleft",
        rotation=0,
        alpha=255,
        on_click=None,
        font_name=None,
        bold=False,
        italic=False
    ):
        """
        Args:
            text: Texte à afficher
            font_size: Taille de la police en pixels
            color: Couleur RGB (R, G, B)
            pos: Position (x, y)
            anchor: Point d'ancrage ("topleft", "center", "topright", etc.)
            rotation: Rotation en degrés
            alpha: Opacité (0-255)
            on_click: Callback appelé au clic sur le texte
            font_name: Nom de la police (None = police par défaut)
            bold: Texte en gras
            italic: Texte en italique
        """
        self._text = text
        self._font_size = font_size
        self._color = color
        self._anchor = anchor
        self._pos = tuple(pos)
        self._rotation = rotation
        self._alpha = max(0, min(255, int(alpha)))
        self._visible = True
        self._on_click = on_click
        self._mouse_down_inside = False
        
        # Police
        self._font_name = font_name
        self._bold = bold
        self._italic = italic
        self._font = self._create_font()
        
        # Cache
        self._cached: Optional[pygame.Surface] = None
        self._cached_size = None
        self._cached_text = None
        
        # Génère la surface initiale
        self._original = self._render_text()
        
        # Enregistrement auprès du manager
        manager = main.widget_manager
        manager.add(self)
        manager.bring_to_front(self)
        
        # Essaye de dessiner immédiatement
        self._try_to_draw_now()

    def _create_font(self) -> pygame.font.Font:
        """Crée l'objet police pygame."""
        # S'assurer que pygame.font est initialisé
        if not pygame.font.get_init():
            pygame.font.init()
        
        try:
            font = pygame.font.Font(self._font_name, self._font_size)
            font.set_bold(self._bold)
            font.set_italic(self._italic)
            return font
        except Exception:
            # Fallback sur la police par défaut
            font = pygame.font.Font(None, self._font_size)
            font.set_bold(self._bold)
            font.set_italic(self._italic)
            return font

    def _render_text(self) -> pygame.Surface:
        """Crée une surface pygame avec le texte rendu."""
        return self._font.render(self._text, True, self._color)

    def _invalidate_cache(self):
        """Invalide le cache pour forcer un re-rendu."""
        self._cached = None
        self._cached_size = None
        self._cached_text = None

    def _get_cached(self) -> pygame.Surface:
        """Retourne la surface en cache, en la créant si nécessaire."""
        # Déterminer si le texte a changé
        if self._cached_text != self._text:
            self._original = self._render_text()
            self._cached_text = self._text
            self._cached = None
        
        # Si cache valide, retourner
        if self._cached is not None:
            return self._cached
        
        surf = self._original
        
        # Redimensionner si nécessaire
        if self._cached_size is not None:
            surf = pygame.transform.scale(surf, self._cached_size)
        
        # Appliquer la rotation
        if self._rotation != 0:
            surf = pygame.transform.rotate(surf, self._rotation)
        
        # Appliquer l'alpha
        if self._alpha < 255:
            surf = surf.copy()
            surf.set_alpha(self._alpha)
        
        self._cached = surf
        return surf

    def kill(self):
        """Supprime le widget du manager."""
        manager = main.widget_manager
        manager.remove(self)
        del self


    def get_rect(self) -> pygame.Rect:
        """Retourne le rectangle du texte."""
        cached = self._get_cached()
        rect = cached.get_rect()
        setattr(rect, self._anchor, self._pos)
        return rect

    def draw(self, surface: pygame.Surface):
        """Dessine le texte sur la surface."""
        if not self._visible:
            return
        
        cached = self._get_cached()
        rect = self.get_rect()
        surface.blit(cached, rect)

    def _try_to_draw_now(self):
        """Essaie de dessiner le texte tout de suite."""
        try:
            if pygame.display.get_init():
                screen = pygame.display.get_surface()
                if screen:
                    self.draw(screen)
                    pygame.display.update(self.get_rect())
                    print(f"📝 Texte affiché immédiatement à {self._pos}")
        except Exception:
            pass

    def set_text(self, text: str):
        """Change le texte."""
        if self._text != text:
            self._text = text
            self._invalidate_cache()

    def set_position(self, pos: Tuple[int, int]):
        """Change la position."""
        self._pos = tuple(pos)

    def set_color(self, color: Tuple[int, int, int]):
        """Change la couleur."""
        if self._color != color:
            self._color = color
            self._original = self._render_text()
            self._invalidate_cache()

    def set_font_size(self, font_size: int):
        """Change la taille de la police."""
        if self._font_size != font_size:
            self._font_size = font_size
            self._font = self._create_font()
            self._invalidate_cache()

    def set_rotation(self, angle: float):
        """Change la rotation (en degrés)."""
        self._rotation = angle % 360
        self._invalidate_cache()

    def set_alpha(self, alpha: int):
        """Change l'opacité."""
        self._alpha = max(0, min(255, int(alpha)))
        self._invalidate_cache()

    def set_size(self, size: Tuple[int, int]):
        """Redimensionne le texte."""
        self._cached_size = tuple(size)
        self._invalidate_cache()

    def set_visible(self, visible: bool):
        """Affiche ou masque le texte."""
        self._visible = visible

    def set_anchor(self, anchor: str):
        """Change le point d'ancrage."""
        self._anchor = anchor

    def set_bold(self, bold: bool):
        """Change le gras."""
        if self._bold != bold:
            self._bold = bold
            self._font = self._create_font()
            self._invalidate_cache()

    def set_italic(self, italic: bool):
        """Change l'italique."""
        if self._italic != italic:
            self._italic = italic
            self._font = self._create_font()
            self._invalidate_cache()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Gère les événements (clic, etc.).
        Retourne True si l'événement est consommé.
        """
        if not self._visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.get_rect().collidepoint(event.pos):
                    self._mouse_down_inside = True
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâchement clic gauche
                if self._mouse_down_inside:
                    self._mouse_down_inside = False
                    if self._on_click and self.get_rect().collidepoint(event.pos):
                        self._on_click()
                    return True
        
        return False

    def get_size(self) -> Tuple[int, int]:
        """Retourne la taille (largeur, hauteur) du texte."""
        cached = self._get_cached()
        return cached.get_size()
