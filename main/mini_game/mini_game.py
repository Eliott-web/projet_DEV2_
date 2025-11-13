class MiniGame:
    def __init__(self, name, description):
        self._name = name
        self._description = description
    
    def __repr__(self):
        return f"Mini-jeu: {self._name} - {self._description}"
    
    
    def start(self):
        print(f"Démarrage du mini-jeu: {self._name}")

    def end(self, success):
        if success:
            print(f"Félicitations! Vous avez réussi le mini-jeu: {self._name}")
        else:
            print(f"Vous avez échoué le mini-jeu: {self._name}. Essayez encore!")

        