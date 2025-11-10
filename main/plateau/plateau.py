class Plateau:
    def __init__(self):
        self._path = []
    
    def __repr__(self):
        return f"Plateau(path='{self.getPathArray}')"

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

    # Getters

    @property
    def getPathArray(self):
        return self._path