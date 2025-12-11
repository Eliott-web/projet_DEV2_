


def makePathWithLength(length): #Créer un chemin de longueur length

    from main.plateau.plateau_utils import makeCase, makePath
    path = makePath()
    for i in range(length):
        case = makeCase()
        path.addCase(case)
    return path