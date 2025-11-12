def movePionOnPath(pion, path, steps):
    """
    Déplace un pion le long d'un chemin spécifique sur le plateau.
    
    Args:
        pion (Pion): Le pion à déplacer.
        path (Path): Le chemin sur lequel déplacer le pion.
        steps (int): Le nombre de cases à déplacer.
    """
    current_position = pion.getCase
    new_position = current_position + steps
    posMax = path.getLength - 1
    reachedEnd = False

    if posMax <= new_position:
        new_position = posMax
        reachedEnd = True
    
    pion.setCase(new_position)
    print("Ce chemin comportre", posMax + 1, "cases." "(index de", 0, "à", posMax,")")
    print("Le pion est à la position :", new_position)
    if reachedEnd:
        print("Le pion a atteint la fin, on l'applaudie !!! 🎉🎉🎉")
    return reachedEnd

def plateauMovePion(plateau, steps):
    pion = plateau.getPion
    path = plateau.getPathArray[pion.getPath]
    return movePionOnPath(pion, path, steps)