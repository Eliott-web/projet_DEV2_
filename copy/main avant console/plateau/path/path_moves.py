


import random


def makePathWithLength(length): #Créer un chemin de longueur length

    from main.plateau.plateau_utils import makeCase, makePath
    path = makePath()
    for i in range(length):
        case = makeCase()
        if random.randint(1, 2) == 1:
            case.setShop(True)
        path.addCase(case)
    return path