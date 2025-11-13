from plateau.plateau import Plateau
from plateau.path.path import Path
from plateau.case.case import Case
from plateau.pion.pion import Pion
from plateau.plateau_moves import plateauMovePion
from plateau.path.path_moves import makePathWithLength

# Y a des fonction utilitaires pour chacunes des classes, mettez un . et vous verrez !


def makePlateau(): #Créer un plateau.
    plat = Plateau()
    return plat

def makePath(): #Créer un chemin
    path = Path()
    return path

def makePathLength(length): #Créer un chemin de longueur length
    return makePathWithLength(length)

def makeCase(): #Créer une case
    case = Case()
    return case

def makePion(): #Créer un pion
    pion = Pion()
    return pion

def movePion(plateau, steps): #Déplacer un pion sur le plateau / RETOURNE si le pion a atteint la fin
    return plateauMovePion(plateau, steps)

def ajouter_item(self, item): 