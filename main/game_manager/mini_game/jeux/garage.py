from main.game_manager.mini_game.controls.control_type_zqsd import ControlTypeZqsd
from main.game_manager.mini_game.entities.mobs.voiture import Car
from main.game_manager.mini_game.entities.objets.parking import Parking
from main.game_manager.mini_game.entities.objets.wall import Wall
from main.game_manager.mini_game.entities.objets.wall import Wall
from main.game_manager.mini_game.mini_game import MiniGame
from main.gui.widget.image import ImageWidget


voitureVitesse = 30
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

    # -----------------------
    #   CONDITIONS VICTOIRE
    # -----------------------

    def winCondition(self):
        return False

    def start(self):
        self.ajouterObjet()
        super().start()

    def ajouterObjet(self):
        self.afficher_fond()
        self.afficher_obstacle(200, 400)
        self.ajouterEntite()

    def ajouterEntite(self):
        posx = self.getCenterXY()[0] - 400
        posy = self.getCenterXY()[1] + 300

        car = Car((posx, posy))
        self.car = car
        self.add_mob(car)

    def afficher_fond(self):
        center = self.getCenterXY()
        sky = ImageWidget("assets/background/parking_background.png",center,(center[0]*2,center[1]*2),
                                      anchor="center",on_click=lambda w: None)
        self.add_object(sky)





        center = self.getCenterXY()

        x_parking = center[0] + 500
        y_parking = center[1] + 300
        pos_parking = (x_parking, y_parking)

        parking = Parking(pos_parking)
        self.parking = parking
        self.add_object(parking)

    def afficher_obstacle(self, wall_x, wall_y):
        center = self.getCenterXY()

        x_obstacle = center[0] + 200
        y_obstacle = center[1] + 200
        pos_obstacle = (x_obstacle, y_obstacle)
        size_obstacle = (wall_x, wall_y)

        # Créer et ajouter l'obstacle
        obstacle = Wall(pos_obstacle, size_obstacle)  # Utiliser la classe Parking comme obstacle
        image = ImageWidget("assets/background/wall.jpg",pos_obstacle,size=size_obstacle,
                                      anchor="center",on_click=lambda w: None)
        obstacle.set_image(image)
        self.add_object(obstacle)

    # voiture controls

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


    def loop(self):
        car = self.car
        if car.get_has_touche_parking():
            self.endInstantly(True)
            return
        
        super().loop()

























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

