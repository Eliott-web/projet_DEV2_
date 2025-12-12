
from controls.control_type_space import ControlTypeSpace
from mini_game import MiniGame

class MiniGameMario(MiniGame, ControlTypeSpace):

    def __init__(self):
        super().__init__("Mario Jump", "Sautez au dessus des tortues!")
        
        self._jumps = 0
        self._required_jumps = 5  # Nombre de sauts requis pour gagner
    
    def winCondition(self):
        return self._jumps >= self._required_jumps

    def space_pressed(self): # Des fonctions à déclarer en fonction du type de contrôle
        self._jumps += 1
        print(f"Jump! Total jumps: {self._jumps}")

    def loop(self): # boucle de jeu si vous en avez besoin de customiser

        print(f"Jump! Total jumps: {self._jumps}") # truc custom

        super().loop()
