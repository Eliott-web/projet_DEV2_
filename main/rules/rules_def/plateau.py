from main.gui import fenetre
from main.rules import rule



class Plateau(rule.Rule):

    def __init__(self):
        super().__init__("plateau", "le fond sera changé pendant un laps de temps")
        # charger l'image
        self.new_background = pygame.image.load("test.png").convert()
        self.new_background = pygame.transform.scale(self.new_background, (WIDTH, HEIGHT))
        self.old_background = None

    def on_add(self, game):
        super().on_add(game)
        # sauvegarder l'ancien fond
        self.old_background = game.current_background
        # remplacer par le nouveau
        game.current_background = self.new_background

    def on_remove(self, game):
        super().on_remove(game)
        if self.old_background is not None:
            game.current_background = self.old_background
