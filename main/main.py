from game_manager.actions import actionInput
from plateau.plateau_utils import *

plat = makePlateau()
path = makePath()
pion = makePion()
case = makeCase()

#path.addCase(case)
path = makePathLength(10)

plat.addPath(path)
plat.setPion(pion)
movePion(plat, 0)
actionInput(plat)