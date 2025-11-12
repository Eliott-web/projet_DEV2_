class Rules:

    def __init__(self):
        self.Rules = {}

    def on_add(self, name, object):
        #ajoute le nom de la règle et la règle du tableau d'objet Rules
        self.Rules[name] = object
        print(f"règles {name} ajouter")

    def on_remove(self, name):
        # retire le nom de la règle et la règle du tableau d'objet Rules
     if name in self.Rules:
         del self.Rules[name]
         print("regles supprimer",name)
     else:
        return print("regles introuvable",name)