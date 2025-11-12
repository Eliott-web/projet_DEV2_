class Plateau:
    def __init__(self):
        self._path = []
        self._pion = None
    
    def __repr__(self):
        return f"Le plateau contient {self.getPathArray}"

    # Setters

    def addPath(self, path):
        self.setPathArray(self.getPathArray + [path])

    def removePath(self, index):
        array = self.getPathArray
        if 0 <= index < len(array):
            del array[index]
            self.setPathArray(array)
        else:
            print("⚠️ Cette index n'existe pas ⚠️")

    def setPathArray(self,path): ## !!! Ca doit être un array
        self._path = path

    def setPion(self, pion):
        self._pion = pion

    # Getters

    @property
    def getPathArray(self):
        return self._path
    
    @property
    def getPion(self):
        return self._pion