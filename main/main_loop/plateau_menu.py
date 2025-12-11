from main.main_loop.main_menu import MainMenu


class PlateauMenu(MainMenu):

    def __init__(self):
        super().__init__()

    def buildPlateau(self):
        plateau = self.getPlateau()

    def makeCase(self):
        pass

    def start(self):
        self.buildPlateau()
        super().start()

    def loop(self):
        
        super().loop()