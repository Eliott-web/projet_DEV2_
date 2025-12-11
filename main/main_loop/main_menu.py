import threading

from main.plateau import plateau


class MainMenu():
    def __init__(self):
         self._objects = []
         self._mobs = []

    def start(self):
        self.loop()

    def getRefreshRate(self):
        from main.game_manager.mini_game.mini_game import MiniGame
        return MiniGame.refresh_rate

    def getRefreshRatePeriod(self):
        return 1 / self.getRefreshRate()

    def getObjects(self):
         return self._objects
    
    def getMobs(self):
        return self._mobs
    
    def getPlateau(self):
        return plateau
    
    def ajouterMob(self):
        self._mobs
    
    def loop(self):

        refreshDelay = self.getRefreshRatePeriod()

        for mob in self.getMobs():
            mob.loop()
        threading.Timer(refreshDelay, self.loop).start() # Continue the loop