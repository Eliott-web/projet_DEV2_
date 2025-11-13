class Item:
    """
    Class pour les items de notre jeu
    """
    def __init__(self, nom, description):
        """
        Création d'un nouvel item dans le jeu
        """
        self.nom = nom
        self.description = description

    def __str__(self):
        """
        Cette méthode spéciale définit ce qui s'affiche
        quand on fait print(mon_item). C'est très pratique !
        """
        return f"Objet: {self.nom} (Info: {self.description})"
    def utiliser(self, joueur):
        """
        Je ne sais pas encore comment utiliser les objects. 
        """
        print(f"{joueur.nom} utilise {self.nom}.")

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.inventaire = []

    def ajouter_item(self, item):

        print(f"[{self.nom} a obtenu : {item.nom}]")
        self.inventaire.append(item)