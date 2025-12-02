class Rule:

    def __init__(self,name,description):
        self._name = name
        self._description = description

    def on_add(self):
        #ajoute le nom de la règle et la règle du tableau d'objet Rules
        print(f"règle {self._name} ajouté")

    def on_remove(self):
        # retire le nom de la règle et la règle du tableau d'objet Rules
       print(f"règle {self._name} retiré")