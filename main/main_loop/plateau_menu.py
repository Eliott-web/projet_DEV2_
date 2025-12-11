from main.game_manager.mini_game.entities.mobs.case_entity import CaseEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.main_loop.main_menu import MainMenu
from main.game_manager.mini_game.controls.controls_getter import ControlsGetter
from pynput import keyboard

case_offset = 300
class PlateauMenu(MainMenu, ControlsGetter):

    def __init__(self):
        super().__init__()
        self._current_case_array = []
        self._old_case_index = 0

    def build(self):
        self.buildPlateau()
        self.buildPion()

    def buildPion(self):
        center = self.getCenterXY()
        pion = PionEntity(center)
        self.getMobs().append(pion)
        x = center[0]

        y_ease = 50
        pion.set_position(x ,pion.get_position()[1] + y_ease)
        pion.set_destination_relative(0 ,-y_ease)

    def buildPlateau(self):
        case_array = self.getCaseArray()
        for i in range(len(case_array)):
            case = self.makeCase(i)
            self.getMobs().append(case)
        

    def makeCase(self, index : int):
        center = self.getCenterXY()
        x = center[0] + (index * case_offset)
        center = (x, center[1] + 60)

        y_ease = 50
        entity = CaseEntity(center)
        entity.set_position(entity.get_position()[0],entity.get_position()[1] + y_ease)
        entity.set_destination_relative(0,-y_ease)

        proprtional_speed = 1/ (index + 1)
        entity.set_vitesse(entity.get_vitesse() * proprtional_speed)

        self.addToCurrentCaseArray(entity)
        return entity
    
    # Actions du joueur

    def initEnd(self):
        print("Le pion a atteint la fin du chemin. Fin du jeu.")

    def moveAll(self):
        plateau = self.getPlateau()
        pion = plateau.getPion
        path = plateau.getPathArray[pion.getPath]
        if pion.getCase >= path.getLength - 1:
            self.initEnd()
            return
        self.avancerPion()
        self.updateCurrentCase()

    def jetDe(self):
        from main.plateau.die.die import lancer_de
        return lancer_de()
    
    def avancerPion(self):
        from main.plateau.plateau_utils import movePion

        de = self.jetDe()
        
        movePion(self.getPlateau(), de)

    def updateCurrentCase(self):
        currentCase = self.getCurrentCaseIndex()
        for case in self.getCurrentCaseArray():
            case.set_destination_relative(-case_offset * (currentCase - self.getOldCaseIndex()), 0)
            case.set_vitesse(50)
        self.setOldCaseIndex(currentCase)

    def addToCurrentCaseArray(self, case):
        self._current_case_array.append(case)

    def getCurrentCaseArray(self):
        return self._current_case_array

    def getCurrentCaseIndex(self):
        pion = self.getPlateau().getPion
        return pion.getCase

    def getCurrentCase(self):
        index = self.getCurrentCaseIndex()
        case_array = self.getCurrentCaseArray()
        if 0 <= index < len(case_array):
            return case_array[index]
        return None
    
    def getOldCaseIndex(self):
        return self._old_case_index
    
    def setOldCaseIndex(self, index):
        self._old_case_index = index

    def getCaseArray(self):
        plateau = self.getPlateau()
        paths = plateau.getPathArray
        if paths:
            path = paths[0]
            return path.getCaseArray
        return []

    def space_on_press(self):
        print("Space pressed - moving all entities")
        self.moveAll()
        """Placeholder invoked when the Space key is pressed."""
        return None

    def e_on_press(self):
        """Placeholder invoked when the 'E' key is pressed."""
        return None
    
    def on_press(self, key):
        if key == keyboard.Key.space:
            self.space_on_press()
    
    def start(self):
        self.build()
        super().start()

    def loop(self):
        self.checkControls()
        super().loop()