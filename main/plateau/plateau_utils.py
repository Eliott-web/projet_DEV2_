from plateau.plateau import Plateau
from plateau.path.path import Path
from plateau.case.case import Case
from plateau.pion.pion import Pion
from plateau.plateau_moves import plateauMovePion

# Y a des fonction utilitaires pour chacunes des classes, mettez un . et vous verrez !


def makePlateau(): #Créer un plateau.
    plat = Plateau()
    return plat

def makePath(): #Créer un chemin
    path = Path()
    return path

def makeCase(): #Créer une case
    case = Case()
    return case

def makePion(): #Créer un pion
    pion = Pion()
    return pion

def movePion(plateau, steps): #Déplacer un pion sur le plateau
    plateauMovePion(plateau, steps)