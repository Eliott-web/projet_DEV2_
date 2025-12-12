class Case:
    def __init__(self):
        self._isShop = False
        pass
    
    def __repr__(self):
        return f"case"
    
    def isShop(self) -> bool:
        return self._isShop
    
    def setShop(self, isShop: bool):
        self._isShop = isShop