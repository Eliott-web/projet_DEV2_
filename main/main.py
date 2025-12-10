from .gui.widget.manager import WidgetManager
from .plateau.plateau_utils import makePlateau

widget_manager = WidgetManager()
plateau = makePlateau()


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