from plateau.plateau_utils import *

plat = makePlateau()
path = makePath()
pion = makePion()
case = makeCase()

path.addCase(case)
path.addCase(case)
path.addCase(case)

plat.addPath(path)
plat.setPion(pion)
movePion(plat, 1)