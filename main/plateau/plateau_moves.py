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
    plateau = pion.getPlateau

    if posMax <= new_position:
        new_position = posMax
        reachedEnd = True
    
    pion.setCase(new_position)
    #print("Ce chemin comportre", posMax + 1, "cases." "(index de", 0, "à", posMax,")")
    showPionPosition(plateau)
    print("Le pion est à la position :", new_position)
    if reachedEnd:
        print("Le pion a atteint la fin, on l'applaudie !!! 🎉🎉🎉")
    return reachedEnd

def plateauMovePion(plateau, steps):
    pion = plateau.getPion
    path = plateau.getPathArray[pion.getPath]
    return movePionOnPath(pion, path, steps)

def showPionPosition(plateau):
    pion = plateau.getPion
    path = plateau.getPathArray[pion.getPath]
    current_position = pion.getCase
    posMax = path.getLength - 1

    # sécurité sur les bornes
    length = posMax + 1
    if length <= 0:
        print("Chemin vide.")
        return

    idx = max(0, min(current_position, posMax))

    # crée une ligne d'underscores et place l'emoji du pion
    positions = ['_'] * length
    positions[idx] = '♟️'
    line = ' '.join(positions)

    print(line)
    print("Position:", idx, "sur", length -1, "cases.")