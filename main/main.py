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
    mainMenu.start()

def setGuiMod(gui):
    global guiMode
    guiMode = gui

def isGuiMode():
    global guiMode
    return guiMode

def buildPlateau():
    path = makePathLength(10)
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