from utils.validators import verifier_nom, verifier_points
from score_utils import ajouter_points_actuel, retirer_points_actuel


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
        self._points = verifier_points(valeur)

    # --- MÉTHODES DU SCORE ---
    def ajouter_points(self, points=3):
        self._points = ajouter_points_actuel(self._points, points)
        print(f"Le joueur {self._joueur} a gagné {points} points. "
              f"Tu as un total de {self._points} points.")

    def retirer_points(self, retrait=3):
        self._points = retirer_points_actuel(self._points, retrait)
        print(f"Le joueur {self._joueur} a perdu {retrait} points. "
              f"Score actuel : {self._points}")

    def afficher_score(self):
        print(f"Votre score est actuellement de {self._points} points.")
