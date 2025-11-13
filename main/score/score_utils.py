def verifier_nom(nom):
    """Vérifie que le nom du joueur est valide (non vide)."""
    if not nom.strip():
        raise ValueError("Le nom du joueur ne peut pas être vide.")
    return nom

def verifier_points(points):
    """Vérifie que le nombre de points est valide (non négatif)."""
    if points < 0:
        raise ValueError("Les points ne peuvent pas être négatifs.")
    return points
