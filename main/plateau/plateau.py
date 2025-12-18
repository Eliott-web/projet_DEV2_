class PlateauException(Exception):
    pass

class PlateauTypeException(PlateauException):
    pass

class PlateauIndexException(PlateauException):
    pass

class PlateauPionException(PlateauException):
    pass


class Plateau:
    def __init__(self):
        self._path = []
        self._pion = None
    
    def __repr__(self):
        return f"Le plateau contient {self.getPathArray}"

    def addPath(self, path):
        try:
            self.setPathArray(self.getPathArray + [path])
        except PlateauTypeException as e:
            raise PlateauTypeException(f"Impossible d'ajouter le chemin : {e}")

    def removePath(self, index):
        array = self.getPathArray
        if 0 <= index < len(array):
            del array[index]
            self.setPathArray(array)
        else:
            raise PlateauIndexException(f"Index {index} invalide pour un tableau de taille {len(array)}")

    def setPathArray(self, path):
        if not isinstance(path, list):
            raise PlateauTypeException(f"Le chemin doit être une liste, pas un {type(path).__name__}")
        self._path = path

    def setPion(self, pion):
        if self._pion is not None:
            raise PlateauPionException("Un pion est déjà présent sur le plateau")
        self._pion = pion
        pion.setPlateau(self)

    @property
    def getPathArray(self):
        return self._path
    
    @property
    def getPion(self):
        return self._pion