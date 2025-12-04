
from ..controls.control_type_space import ControlTypeSpace
from ..mini_game import MiniGame
from ..entities.mobs.mob import Mob

class MiniGameMario(MiniGame, ControlTypeSpace):

    def __init__(self):
        super().__init__("Mario Jump", "Sautez au dessus des tortues!")
        
        self._jumps = 0
        self._required_jumps = 5  # Nombre de sauts requis pour gagner

        mob = Mob("Tortue1", 0.5, (2, 2))
        mob.set_destination(1.7, 0)
        self.add_mob(mob)
    
    def winCondition(self):
        return self._jumps >= self._required_jumps

    def space_pressed(self):
        self._jumps += 1

    def loop(self): # boucle de jeu si vous en avez besoin de customiser

        #print(f"Jump! Total jumps: {self._jumps}") # truc custom

        super().loop()