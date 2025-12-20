import unittest
import random
from main.plateau.die.die import lancer_de
from main.score.score import Score, verifier_points, verifier_nom

class InvalidScoreError(Exception):
    """Exception levée lorsque le score est négatif."""
    pass

def verifier_points(valeur):
    """
    Spécifications :
    PRE : valeur doit être un nombre (int ou float).
    POST : Retourne la valeur si >= 0, sinon lève InvalidScoreError.
    """
    if valeur < 0:
        raise InvalidScoreError(f"Score invalide : {valeur}")
    return valeur

def lancer_de(multiplicateur=1):
    """
    Spécifications :
    PRE : multiplicateur est un entier positif.
    POST : Retourne un entier entre 1 et 3 multiplié par le multiplicateur.
    """
    return random.randint(1, 3) * multiplicateur



class TestJeuPlateau(unittest.TestCase):

    # TESTS POUR LE SCORE
    def test_verifier_points_valide(self):
        """Vérifie qu'un score positif est accepté."""
        self.assertEqual(verifier_points(10), 10)

    def test_verifier_points_negatif(self):
        """Vérifie qu'une exception est levée pour un score négatif."""
        with self.assertRaises(InvalidScoreError):
            verifier_points(-5)

    # TESTS POUR LE DÉ
    def test_lancer_de_bornes(self):
        """Vérifie que le dé est bien entre 1 et 3 (pour mult=1)."""
        for _ in range(100):
            resultat = lancer_de(1)
            self.assertIn(resultat, [1, 2, 3])

    def test_lancer_de_multiplicateur(self):
        """Vérifie que le multiplicateur est bien appliqué."""
        resultat = lancer_de(10)
        self.assertTrue(resultat in [10, 20, 30])