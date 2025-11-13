from .score_utils import verifier_nom, verifier_points

class Score:
    basePoints = 5

    def __init__(self, joueur):
        self._joueur = verifier_nom(joueur)
        self._points = Score.basePoints

    # --- GETTERS / SETTERS ---
    @property
    def joueur(self):
        return self._joueur

    @joueur.setter
    def joueur(self, nouveau_nom):
        self._joueur = verifier_nom(nouveau_nom)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, valeur):
        valeur = verifier_points(valeur)
        self._points = valeur

    # --- MÉTHODES DU SCORE ---
    def ajouter_points(self, points=3):
        verifier_points(points)
        self._points += points
        print(f"Le joueur {self._joueur} a gagné {points} points. "
              f"Tu as un total de {self._points} points.")

    def retirer_points(self):
        self._points -= 3
        if self._points < 0:
            self._points = 0
        print(f"Le joueur {self._joueur} a perdu 3 points. "
              f"Score actuel : {self._points}")

    def afficher_score(self):
        print(f"Votre score est actuellement de {self._points} points.")
