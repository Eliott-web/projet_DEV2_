def verifier_nom(nom: str) -> str:
    """Vérifie que le nom du joueur est valide (non vide)."""
    if not isinstance(nom, str):
        raise TypeError("Le nom doit être une chaîne de caractères.")
    if not nom.strip():
        raise ValueError("Le nom du joueur ne peut pas être vide.")
    return nom.strip()


def verifier_points(points: int) -> int:
    """Vérifie que le nombre de points est valide (non négatif)."""
    if not isinstance(points, (int, float)):
        raise TypeError("Les points doivent être un nombre.")
    if points < 0:
        raise ValueError("Les points ne peuvent pas être négatifs.")
    return int(points)