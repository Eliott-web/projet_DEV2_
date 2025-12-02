def makePathWithLength(length): #Créer un chemin de longueur length
    from plateau.plateau_utils import makePath
    from plateau.plateau_utils import makeCase

    path = makePath()
    for i in range(length):
        case = makeCase()
        path.addCase(case)
    return path