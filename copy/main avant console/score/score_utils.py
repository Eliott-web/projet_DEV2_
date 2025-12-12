from .validators import verifier_points


def ajouterPoints(score, points):
    points0 = score.points
    points0 += verifier_points(points)
    return points0

def retirerPoints(score, retrait):
    points0 = score.points
    points0 -= verifier_points(retrait)
    if points0 < 0:
        points0 = 0
    return points0
