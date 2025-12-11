from projet_DEV2_.main.game_manager.mini_game.controls.control_type_zqsd import ControlTypeZqsd
from projet_DEV2_.main.game_manager.mini_game.entities.mobs.voiture import Car
from projet_DEV2_.main.game_manager.mini_game.entities.objets.parking import Parking
from projet_DEV2_.main.game_manager.mini_game.mini_game import MiniGame

voitureVitesse = 25
class MiniGameGarage(MiniGame, ControlTypeZqsd):

    def __init__(self):
        super().__init__("Parking Challenge", "Garez la voiture sur la place marquée !")

        self.car = None
        self.Ground = True

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

    def start(self):
        self.ajouterObjet()
        super().start()

    def ajouterObjet(self):
        self.afficher_fond()
        self.ajouterAntiter()

    def ajouterAntiter(self):
        car = Car(self.getCenterXY())
        self.car = car
        self.add_mob(car)

    def afficher_fond(self):
        center = self.getCenterXY()

        x_parking = center[0] + 100
        y_parking = center[1]
        pos_parking = (x_parking, y_parking)

        parking = Parking(pos_parking)
        self.parking = parking
        self.add_object(parking)

    def up_pressed(self):
        global voitureVitesse
        car = self.car
        car.set_velocity(0, -voitureVitesse)

    def down_pressed(self):
        global voitureVitesse
        car = self.car
        car.set_velocity(0, voitureVitesse)

    def right_pressed(self):
        global voitureVitesse
        car = self.car
        car.set_velocity(voitureVitesse, 0)

    def left_pressed(self):
        global voitureVitesse
        car = self.car
        car.set_velocity(-voitureVitesse, 0)




























    def checkCollision(self):
        if (self._car_x, self._car_y) in self._obstacles:
            print("💥 Collision avec un obstacle !")
            self._crashed = True



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