import time
import threading
from .mobs.mob import Mob
from .controls.controls_getter import ControlsGetter

class MiniGame(ControlsGetter):
    default_time_limit = 3  # secondes
    refresh_rate = 20  # FPS
    
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._time_limit = MiniGame.default_time_limit
        self._timer = 0
        self._mobs = []
    
    def __repr__(self):
        return f"Mini-jeu: {self._name} - {self._description}"
    
    
    def start(self):
        print(f"Démarrage du mini-jeu: {self._name}")
        self.reset_timer()
        self.loop()

    def end(self, success):

        if success:
            print(f"Félicitations! Vous avez réussi le mini-jeu: {self._name}")
        else:
            print(f"Vous avez échoué le mini-jeu: {self._name}. Essayez encore!")
        

    #  mob methods
    def add_mob(self, mob):
        self._mobs.append(mob)

        


    #  Timer methods
    def update_timer(self):
        timer = self.getTimer()
        timeLimit = self.getTimeLimit()
        
        timer += self.gerRefreshRatePeriod()
        self._timer = timer
        if timer >= timeLimit:
            return True # time's up
        return False

    def reset_timer(self):
        self._timer = 0

    def getTimer(self):
        return self._timer
    
    def getTimeLimit(self):
        return self._time_limit
    

    # Loop methods
    def winCondition(self): # ⚠️ Definir dans le mini-jeu ⚠️
        return False

    def getRefreshRate(self):
        return MiniGame.refresh_rate
    
    def gerRefreshRatePeriod(self):
        return 1 / self.getRefreshRate()
    
    def loop(self):

        self.checkControls() # Check for user inputs

        refreshDelay = self.gerRefreshRatePeriod()
        end = self.update_timer()
        win = self.winCondition()
        
        if (end | win):
            self.end(win)
            return  # End the loop
        
        #print(f"Timer: {self.getTimer():.2f}s / {self.getTimeLimit()}s")
        for mob in self._mobs:
            mob.loop()
        threading.Timer(refreshDelay, self.loop).start() # Continue the loop
        