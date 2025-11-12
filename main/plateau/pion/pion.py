class Pion:
    def __init__(self):
        self._case = 0
        self._path = 0
    
    def __repr__(self):
        return f"case"
    
    # Setters

    def setCase(self, case):
        self._case = case
    
    def setPath(self, path):
        self._path = path

    # Getters

    @property
    def getCase(self):
        return self._case
    
    @property
    def getPath(self):
        return self._path