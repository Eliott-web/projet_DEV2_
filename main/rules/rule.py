class Rule:

    def __init__(self,name,description):
        self.name = name
        self.description = description

    def on_add(self):
        #ajoute le nom de la règle et la règle du tableau d'objet Rules
        print(f"règle {self.name} ajouté")

    def on_remove(self):
        # retire le nom de la règle et la règle du tableau d'objet Rules
       print(f"règle {self.name} retiré")

    def getName(self):
        return self.name
    def getDescription(self):
        return self._description