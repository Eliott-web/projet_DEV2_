from validators import verifier_points


def ajouter_points_actuel(points_actuels: int, ajout: int) -> int:
    verifier_points(ajout)
    return points_actuels + ajout


def retirer_points_actuel(points_actuels: int, retrait: int = 3) -> int:
    points_actuels -= retrait
    return max(points_actuels, 0)
