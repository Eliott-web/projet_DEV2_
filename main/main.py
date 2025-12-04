from game_manager.actions_utils import initGamePlay
from plateau.plateau_utils import *
from score.score import Score
from game_manager.mini_game.jeux.garage import MiniGameGarage


joueur1 = Score("Eliott")

car = MiniGameGarage()
print(car)

car.start()

'''
plat = makePlateau()
path = makePath()
pion = makePion()
case = makeCase()

pion.setScore(joueur1)

#path.addCase(case)
path = makePathLength(10)

plat.addPath(path)
plat.setPion(pion)
movePion(plat, 0)
initGamePlay(plat)
'''