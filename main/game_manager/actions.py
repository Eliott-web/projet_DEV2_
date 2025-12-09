from plateau.plateau_utils import *
from plateau.die.die import lancer_de


def actionInput(plateau):
    reponse = input("Voulez-vous lancer le dé ? (oui/non) ").lower()
    if reponse != "oui":
        print("Fin du tour.")
        return

    # Lancer le dé
    steps = lancer_de()
    print(f"Vous avez obtenu : {steps}")

    # Déplacer le pion
    reachedEnd = movePion(plateau, steps)
    if reachedEnd:
        return

    # Re-demander si le joueur veut relancer
    actionInput(plateau)
