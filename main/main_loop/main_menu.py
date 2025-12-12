import threading

from main import main


class MainMenu():
    def __init__(self):
         self._objects = []
         self._mobs = []
         self._paused = False

    def start(self):
        self.loop_start()

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
        return main.plateau
    
    def ajouterMob(self):
        self._mobs

    def ajouterObject(self, obj):
        self._objects.append(obj)

    def getCenterXY(self):
        from main.gui.fenetre import HEIGHT, WIDTH
        return (WIDTH // 2, HEIGHT // 2)
    
    def setPaused(self, paused: bool):
        if self._paused == paused:
            return
        self._paused = paused
        if not paused:
            self.loop_start()

    def loop_start(self):
        self.loop()

    def isPaused(self) -> bool:
        return self._paused
    
    def stop(self):
        for obj in self.getObjects():
            obj.kill()

        for mob in self.getMobs():
            mob.kill()

        self._mobs.clear()
        self._objects.clear()
        self.setPaused(True)
        del self

    def loop(self):
        if self.isPaused():
            return
        
        refreshDelay = self.getRefreshRatePeriod()

        for mob in self.getMobs():
            mob.loop()
        threading.Timer(refreshDelay, self.loop).start() # Continue the loop