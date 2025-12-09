# main/gui/widget/manager.py
from typing import List, Callable

class WidgetManager:
    """
    Gestionnaire simple de widgets.
    - stocke les widgets dans une liste (ordre = z-order, dernière = au dessus)
    - draw_all(surface) dessine tous les widgets
    - update_all(dt) appelle 'update(dt)' si présent
    - handle_event(evt) propage les événements (clics, etc.)
    """
    
    def __init__(self):
        self._widgets: List = []

    def add(self, widget, index: int = None):
        """Ajoute un widget. Par défaut en haut (fin de liste)."""
        if index is None:
            self._widgets.append(widget)
        else:
            self._widgets.insert(index, widget)

    def remove(self, widget):
        try:
            self._widgets.remove(widget)
        except ValueError:
            pass

    def clear(self):
        self._widgets.clear()

    def bring_to_front(self, widget):
        self.remove(widget)
        self.add(widget)

    def send_to_back(self, widget):
        self.remove(widget)
        self.add(widget, 0)

    def draw_all(self, surface):
        """Dessine tous les widgets dans l'ordre."""
        for w in self._widgets:
            draw = getattr(w, "draw", None)
            if callable(draw):
                draw(surface)

    def update_all(self, dt):
        """Appelez dans la boucle principale; dt = temps écoulé en secondes."""
        for w in list(self._widgets):
            upd = getattr(w, "update", None)
            if callable(upd):
                try:
                    upd(dt)
                except Exception:
                    pass

    def handle_event(self, event):
        """
        Propagation d'événements :
        - Pour un clic souris, on parcourt la liste à l'envers (top-down) et on stoppe si consommé.
        - Appelle 'handle_event(event)' sur chaque widget si disponible.
        """
        # gestion click pour widgets top-down
        if event.type in (32768,):  # pygame.USEREVENT fallback - but better to import pygame; we won't rely on hardcoded values
            pass

        # generic propagation: top-down, widget peut retourner True pour indiquer qu'il a consommé l'événement
        for w in reversed(self._widgets):
            handler = getattr(w, "handle_event", None)
            if callable(handler):
                try:
                    consumed = handler(event)
                except Exception:
                    consumed = False
                if consumed:
                    return True
        return False

    def widgets(self):
        return list(self._widgets)