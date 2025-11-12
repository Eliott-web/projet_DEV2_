from plateau.plateau_utils import *

def actionInput(plateau):
    steps = int(input("Combien de pas voulez-vous avancer le pion ? "))
    reachedEnd = movePion(plateau, steps)
    if reachedEnd:
        return
    actionInput(plateau)
    print("")