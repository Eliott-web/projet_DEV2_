import random

#Fonction qui simule un lancer de dé
multiplicateur = 1
def lancer_de():
    return random.randint(1, 3) * multiplicateur

#print('Tu as obtenu :', lancer_de())