from ..controls.control_type_zqsd import ControlTypeSpace
from ..mini_game import MiniGame

class MiniGameGarage(MiniGame, ControlTypeSpace):

    def __init__(self):
        super().__init__("Parking Challenge", "Garez la voiture sur la place marquée !")

        # Taille de la grille
        self._width = 10
        self._height = 10

        # Position de la voiture
        self._car_x = 0
        self._car_y = 0

        # Position cible
        self._target_x = 5
        self._target_y = 3

        # Obstacles
        self._obstacles = [
            (2, 0),
            (2, 1),
            (3, 2),
            (4, 3)
        ]

        self._crashed = False

    # -----------------------
    #   CONDITIONS VICTOIRE
    # -----------------------

    def winCondition(self):
        if self._crashed:
            return False
        return self._car_x == self._target_x and self._car_y == self._target_y

    # -----------------------
    #     COLLISION
    # -----------------------

    def checkCollision(self):
        if (self._car_x, self._car_y) in self._obstacles:
            print("💥 Collision avec un obstacle !")
            self._crashed = True

    # -----------------------
    #       CONTROLES
    # -----------------------

    def up_pressed(self):
        self._car_y -= 1
        self.checkCollision()

    def down_pressed(self):
        self._car_y += 1
        self.checkCollision()

    def left_pressed(self):
        self._car_x -= 1
        self.checkCollision()

    def right_pressed(self):
        self._car_x += 1
        self.checkCollision()

    # -----------------------
    #   AFFICHAGE ASCII
    # -----------------------

    def display_grid(self):
        print("\n===== PARKING =====")

        for y in range(self._height):
            row = ""
            for x in range(self._width):

                # Voiture ?
                if x == self._car_x and y == self._car_y:
                    cell = "🚗"

                # Place de parking ?
                elif x == self._target_x and y == self._target_y:
                    cell = "🅿️"

                # Obstacle ?
                elif (x, y) in self._obstacles:
                    cell = "⬛"

                else:
                    cell = "."

                row += cell

            print(row)

        print("====================\n")

    # -----------------------
    #        LOOP
    # -----------------------

    def loop(self):
        self.display_grid()

        if self._crashed:
            print("🚫 La voiture est détruite, vous avez perdu.")

        super().loop()