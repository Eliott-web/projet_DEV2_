class Pion:
    def __init__(self):
        self._case = 0
        self._path = 0
        self._plateau = None
        self._inventaire = []
    
    def __repr__(self):
        return f"case"
    
    # Setters

    def setCase(self, case):
        self._case = case
    
    def setPath(self, path):
        self._path = path

    def setPlateau(self, plateau):
        self._plateau = plateau

    def ajouter_item(self, item):

        print(f"[Tu as obtenu : {item}]")
        self._inventaire.append(item)

    # Getters

    @property
    def getCase(self):
        return self._case
    
    @property
    def getPath(self):
        return self._path
    
    @property
    def getPlateau(self):
        return self._plateau
    
    @property
    def getInventaire(self):
        return self._inventaire