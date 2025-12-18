import re
from functools import wraps


def validate_index(func):
    @wraps(func)
    def wrapper(self, index, *args, **kwargs):
        if not isinstance(index, int):
            print("⚠️ L'index doit être un entier ⚠️")
            return None
        if index < 0 or index >= len(self.getCaseArray):
            print("⚠️ Cette index n'existe pas ⚠️")
            return None
        return func(self, index, *args, **kwargs)
    return wrapper


class Path:
    def __init__(self):
        self._case = []
        # Expression régulière pour valider le format des IDs de case (exemple: "C1", "C10", etc.)
        self._case_id_pattern = re.compile(r'^[A-Z]\d+$')
    
    def __repr__(self):
        return f"Path = {self.getCaseArray}"

    # Setters

    def addCase(self, case):
        self.setCaseArray(self.getCaseArray + [case])

    @validate_index
    def removeCase(self, index):
        """Retire une case à l'index spécifié (utilise le décorateur pour validation)"""
        array = self.getCaseArray
        del array[index]
        self.setCaseArray(array)

    def setCaseArray(self, case): ## !!! Ca doit être un array
        self._case = case

    # Getters

    @property
    def getCaseArray(self):
        return self._case
    
    @property
    def getLength(self):
        return len(self._case)
    
    def filterCases(self, condition):
        filter_func = lambda case: condition(case)
        return list(filter(filter_func, self.getCaseArray))
    
    def validateCaseId(self, case_id):
        return bool(self._case_id_pattern.match(case_id))
    
    def getCasesWithValidId(self):
        return list(filter(lambda case: hasattr(case, 'id') and self.validateCaseId(str(case.id)), 
                          self.getCaseArray))