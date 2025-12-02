from .validators import verifier_nom, verifier_points
from .score_utils import ajouterPoints, retirerPoints

class Score:
    basePoints = 5

    baseAddPoints = 3

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
        self._points = verifier_points(valeur)

    # --- MÉTHODES DU SCORE ---
    def ajouterPoints(self, points=3):
        self._points = ajouterPoints(self, points=Score.baseAddPoints)
        print(f"Le joueur {self._joueur} a gagné {points} points. "
              f"Tu as un total de {self._points} points.")

    def retirerPoints(self, retrait= baseAddPoints):
        self._points = retirerPoints(self, retrait)
        print(f"Le joueur {self._joueur} a perdu {retrait} points. "
              f"Score actuel : {self._points}")

    def afficherScore(self):
        print(f"Votre score est actuellement de {self._points} points.")
