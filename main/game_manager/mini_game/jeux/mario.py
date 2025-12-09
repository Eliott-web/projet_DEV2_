
from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.gui.widget.image import ImageWidget
from main.main import widget_manager
from ..controls.control_type_space import ControlTypeSpace
from ..mini_game import MiniGame
from ..entities.mobs.mob import Mob

class MiniGameMario(MiniGame, ControlTypeSpace):

    def __init__(self):
        super().__init__("Mario Jump", "Sautez au dessus des tortues!")
        
        self._jumps = 0
        self._required_jumps = 5  # Nombre de sauts requis pour gagner
    
    def winCondition(self):
        return self._jumps >= self._required_jumps

    def space_pressed(self):
        self._jumps += 1

    def start(self):
        print("Démarrage du mini-jeu Mario Jump!")
        self.ajouterKoopa()
        super().start()

    def ajouterKoopa(self):
        koopa = Koopa(self.getCenterXY())
        self.add_mob(koopa)
        koopa.set_destination_relative(300, 500)  # Déplace la koopa vers le bas

    def loop(self): # boucle de jeu si vous en avez besoin de customiser

        #print(f"Jump! Total jumps: {self._jumps}") # truc custom

        super().loop()