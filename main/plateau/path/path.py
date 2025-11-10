class Path:
    def __init__(self):
        self._case = []
    
    def __repr__(self):
        return f"Case(case='{self.getCaseArray}')"

    # Setters

    def addCase(self, case):
        self.setCaseArray(self.getCaseArray + [case])

    def removeCase(self, index):
        array = self.getCaseArray
        if 0 <= index < len(array):
            del array[index]
            self.setCaseArray(array)
        else:
            print("⚠️ Cette index n'existe pas ⚠️")

    def setCaseArray(self,case): ## !!! Ca doit être un array
        self._case = case

    # Getters

    @property
    def getCaseArray(self):
        return self._case