from main.main_loop.main_menu import MainMenu
from main.main_loop.plateau_menu import PlateauMenu
from main.plateau.pion.pion import Pion
from .gui.widget.manager import WidgetManager
from .plateau.plateau_utils import makePathLength, makePlateau

widget_manager = WidgetManager()
plateau = makePlateau()
mainMenu = PlateauMenu()
guiMode = False

def init():
    buildPlateau()
    
    if guiMode:
        # Mode GUI
        mainMenu.start()
    else:
        # Mode Console
        from main.console.console_game_manager import ConsoleGameManager
        console_manager = ConsoleGameManager(plateau)
        console_manager.start()

def setGuiMod(gui):
    global guiMode
    guiMode = gui

def isGuiMode():
    global guiMode
    return guiMode

def buildPlateau():
    # Mode console : 5 cases, Mode GUI : 15 cases
    length = 5 if not guiMode else 15
    path = makePathLength(length)
    plateau.addPath(path)
    plateau.setPion(Pion())


'''

plat = makePlateau()
path = makePath()
pion = makePion()
case = makeCase()

pion.setScore(joueur1)

#path.addCase(case)
path = makePathLength(30)

plat.addPath(path)
plat.setPion(pion)
step = lancer_de()
movePion(plat, step)
initGamePlay(plat)
'''