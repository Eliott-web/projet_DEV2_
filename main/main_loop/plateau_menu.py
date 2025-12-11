from main.game_manager.mini_game.entities.mobs.case_entity import CaseEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.main_loop.main_menu import MainMenu


class PlateauMenu(MainMenu):

    def __init__(self):
        super().__init__()
        self._current_case_array = []

    def build(self):
        self.buildPlateau()
        self.buildPion()

    def buildPion(self):
        center = self.getCenterXY()
        pion = PionEntity(center)
        self.getMobs().append(pion)

    def buildPlateau(self):
        case_array = self.getCaseArray()
        for i in range(len(case_array)):
            case = self.makeCase(i)
            self.getMobs().append(case)
        

    def makeCase(self, index : int):
        center = self.getCenterXY()
        x = center[0] + (index* 150)
        center = (x, center[1] + 60)

        y_ease = 50
        entity = CaseEntity(center)
        entity.set_position(entity.get_position()[0],entity.get_position()[1] + y_ease)
        entity.set_destination_relative(0,-y_ease)

        proprtional_speed = 1/ (index + 1)
        entity.set_vitesse(entity.get_vitesse() * proprtional_speed)

        self.addToCurrentCaseArray(entity)
        return entity
    
    def addToCurrentCaseArray(self, case):
        self._current_case_array.append(case)

    def getCurrentCaseArray(self):
        return self._current_case_array


    def getCaseArray(self):
        plateau = self.getPlateau()
        path = plateau.getPathArray
        return path.getCaseArray

    def start(self):
        self.build()
        super().start()

    def loop(self):
        
        super().loop()