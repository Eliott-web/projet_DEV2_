from game_manager.actions_utils import initGamePlay
from plateau.plateau_utils import *
from score.score import Score


joueur1 = Score("Eliott")

joueur1.afficher_score()


plat = makePlateau()
path = makePath()
pion = makePion()
case = makeCase()

#path.addCase(case)
path = makePathLength(10)

plat.addPath(path)
plat.setPion(pion)
movePion(plat, 0)
initGamePlay(plat)