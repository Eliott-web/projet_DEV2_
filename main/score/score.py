import random

class Score:
    #Valeur de base
    basePoints = 5
    def __init__(self, jouer):
        self.jouer = jouer          #nom du jouer
        self.points = Score.basePoints            #création du score initial de 5 car on veut que le joueur commece avec 5 pièces

    def ajouter_points(self, min_points = 1, max_points = 15):
        #on ajoute les points au joueur aléatoirement entre 1 et 15
        nbr = random.randint(min_points, max_points)
        self.points += nbr
        print(f"le jouer ${self.jouer} a gagné {nbr} points. Tu as un total de {self.points} points.")  #message pour vérifier le bon fonctionnement

    def retirer_points(self):
        self.points -= 3
        #vérifier si le joueur a encore des points
        if self.points < 0:
            self.points = 0     #on dit que le score ne peut pas être négatif

        print(f"Vous avez perdu, vous n'avez plus de points.")

    def reset_scores(self):
        self.points = Score.basePoints
        print(f"Le score a été remis à ${self.points} points.")

    def afficher_score(self):
        print(f"Votre score est actuellement de {self.points} points.")
